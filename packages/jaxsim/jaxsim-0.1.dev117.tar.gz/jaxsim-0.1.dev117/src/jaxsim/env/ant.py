from pathlib import Path
from typing import Tuple, ClassVar

import jax
import jax.numpy as jnp
import jax_dataclasses

from jaxsim import high_level
from jaxsim.gym import Env, EnvironmentState
from jaxsim.gym.spaces import Box
from jaxsim.gym.typing import *
from jaxsim.physics.algos.soft_contacts import SoftContactsParams
from jaxsim.simulation.simulator import JaxSim, SimulatorData
from jaxsim.utils import JaxsimDataclass


@jax_dataclasses.pytree_dataclass
class AntObservation(JaxsimDataclass):

    base_height: jtp.Float
    gravity_projection: jtp.Array
    joint_positions: jtp.Array
    joint_velocities: jtp.Array
    base_linear_velocity: jtp.Array
    base_angular_velocity: jtp.Array
    contact_state: jtp.Array
    # TODO: feet_contact_status: jtp.Array
    # TODO: forces?


@jax_dataclasses.pytree_dataclass
class AntEnvironment(Env):

    name: ClassVar = jax_dataclasses.static_field(default="ant")

    @staticmethod
    def build() -> Tuple["AntEnvironment", EnvironmentState]:

        T = 0.050
        # dt = 0.000_200
        dt = 0.000_500

        simulator = JaxSim(
            step_size=dt,
            steps_per_run=int(T / dt),
            velocity_representation=high_level.model.VelRepr.Body,
            data=SimulatorData(
                gravity=jnp.array([0, 0, -10.0]),
                contact_parameters=SoftContactsParams(K=5_000, D=10),
            ),
        )

        with simulator.editable(validate=False) as simulator:

            simulator: JaxSim
            sdf_path = Path("~/git/jaxsim/examples/resources/ant2.sdf")  # TODO
            _ = simulator.insert_model_from_sdf(sdf=sdf_path.expanduser().absolute())

        with EnvironmentState().editable(validate=False) as state:
            state.simulator = simulator

        with AntEnvironment(_action_space=None, _observation_space=None).editable(
            validate=False
        ) as env:

            env._action_space = env.build_action_space(state=state)
            env._observation_space = env.build_observation_space(state=state)

        return env, EnvironmentState.to_jax(state=state)

    def build_action_space(self, state: EnvironmentState) -> Box:

        model = state.simulator.get_model(model_name="ant")

        high = 50.0 * jnp.ones(model.dofs())
        return Box(low=-high, high=high)

    def build_observation_space(self, state: EnvironmentState) -> Box:

        model = state.simulator.get_model(model_name="ant")
        s_min, s_max = model.joint_limits()

        low = AntObservation(
            base_height=0.15,
            gravity_projection=-jnp.ones(3),
            joint_positions=s_min,
            joint_velocities=-4.0 * jnp.ones_like(s_min),
            base_linear_velocity=-5.0 * jnp.ones(3),
            base_angular_velocity=-10.0 * jnp.ones(3),
            contact_state=jnp.array([False] * 8, dtype=bool),
        )

        high = AntObservation(
            base_height=1.0,
            gravity_projection=jnp.ones(3),
            joint_positions=s_max,
            joint_velocities=4.0 * jnp.ones_like(s_max),
            base_linear_velocity=5.0 * jnp.ones(3),
            base_angular_velocity=10.0 * jnp.ones(3),
            contact_state=jnp.array([True] * 8, dtype=bool),
        )

        return Box(low=low, high=high)

    def initial_distribution(self, state: EnvironmentState) -> Box:

        model = state.simulator.get_model(model_name="ant")
        s_min, s_max = model.joint_limits()
        range = s_max - s_min
        s_min += 0.1 * range
        s_max -= 0.1 * range

        low = AntObservation(
            base_height=0.6,
            gravity_projection=jnp.zeros(3),
            joint_positions=s_min,
            joint_velocities=-0.5 * jnp.ones_like(s_min),
            base_linear_velocity=-0.1 * jnp.ones(3),
            base_angular_velocity=-0.5 * jnp.ones(3),
            contact_state=jnp.array([False] * 8, dtype=bool),
        )

        high = AntObservation(
            base_height=0.7,
            gravity_projection=jnp.zeros(3),
            joint_positions=s_max,
            joint_velocities=0.5 * jnp.ones_like(s_max),
            base_linear_velocity=0.1 * jnp.ones(3),
            base_angular_velocity=0.5 * jnp.ones(3),
            contact_state=jnp.array([False] * 8, dtype=bool),
        )

        return Box(low=low, high=high)

    def get_observation(self, state: EnvironmentState) -> Observation:

        model = state.simulator.get_model(model_name="ant")

        B_R_W = jnp.linalg.inv(model.base_orientation(dcm=True))
        W_gravity = state.simulator.gravity()
        B_gravity = B_R_W @ (W_gravity / jnp.linalg.norm(W_gravity))

        return AntObservation(
            base_height=model.base_position()[2],
            gravity_projection=B_gravity,
            joint_positions=model.joint_positions(),
            joint_velocities=model.joint_velocities(),
            base_linear_velocity=model.base_velocity()[0:3],
            base_angular_velocity=model.base_velocity()[3:6],
            contact_state=jnp.array(
                [
                    model.get_link(name).in_contact()
                    for name in model.link_names()
                    if "leg_" in name
                ],
                dtype=bool,
            ),
        )

    def reset(
        self, state: EnvironmentState, **kwargs
    ) -> Tuple[EnvironmentState, Observation]:

        initial_distribution = self.initial_distribution(state=state)

        subkey, state = state.generate_key()
        observation: AntObservation = initial_distribution.sample(key=subkey)

        with state.editable(validate=True) as state:

            model = state.simulator.get_model(model_name="ant")
            model.zero()

            model.reset_base_position(
                position=jnp.array([0, 0, observation.base_height])
            )
            model.reset_joint_positions(positions=observation.joint_positions)
            model.reset_joint_velocities(velocities=observation.joint_velocities)
            model.reset_base_velocity(
                base_velocity=jnp.hstack(
                    [
                        observation.base_linear_velocity,
                        observation.base_angular_velocity,
                    ]
                )
            )

        return state, self.get_observation(state)

    def step(
        self, action: Action, state: EnvironmentState
    ) -> Tuple[EnvironmentState, Tuple[Observation, Reward, IsDone, Info]]:

        with state.editable() as state:

            model = state.simulator.get_model(model_name="ant")

            model.zero_input()
            # model.set_joint_generalized_force_targets(forces=action)
            model.set_joint_generalized_force_targets(forces=jnp.zeros_like(action))

            state.simulator.step()

        observation = self.get_observation(state=state)

        is_done = jax.lax.select(
            pred=self.observation_space.contains(x=observation),
            on_true=False,
            on_false=True,
        )

        alive = 1.0 - jnp.array(is_done, dtype=int)

        reward = alive
        reward += model.base_velocity()[0]
        reward -= 0.001 * jnp.sum(jnp.square(action))  # TODO

        # return state, (observation, reward, is_done, FrozenDict())

        info = FrozenDict(
            dict(
                f_ext={
                    name: model.get_link(name).external_force()
                    for name in model.link_names()
                    if "leg_" in name
                }
            )
        )

        return state, (observation, reward, is_done, info)
