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
class CartpoleObservation(JaxsimDataclass):

    linear_pos: jtp.Float
    linear_vel: jtp.Float
    pivot_pos: jtp.Float
    pivot_vel: jtp.Float


@jax_dataclasses.pytree_dataclass
class CartpoleEnvironment(Env):

    name: ClassVar = jax_dataclasses.static_field(default="cartpole")

    @staticmethod
    def build() -> Tuple["CartpoleEnvironment", EnvironmentState]:

        T = 0.010
        dt = 0.000_200

        simulator = JaxSim(
            step_size=dt,
            steps_per_run=int(T / dt),
            velocity_representation=high_level.model.VelRepr.Body,
            data=SimulatorData(gravity=jnp.array([0, 0, -10.0])),
        )

        with simulator.editable(validate=False) as simulator:

            simulator: JaxSim
            sdf_path = Path("~/git/jaxsim/examples/resources/cartpole.sdf")
            _ = simulator.insert_model_from_sdf(sdf=sdf_path.expanduser().absolute())
            # TODO: disable contacts?

        with EnvironmentState().editable(validate=False) as state:
            state.simulator = simulator

        with CartpoleEnvironment(_action_space=None, _observation_space=None).editable(
            validate=False
        ) as env:

            env._action_space = env.build_action_space(state=state)
            env._observation_space = env.build_observation_space(state=state)

        return env, EnvironmentState.to_jax(state=state)

    def build_action_space(self, state: EnvironmentState) -> Box:

        return Box(low=-50.0, high=50.0)

    def build_observation_space(self, state: EnvironmentState) -> Box:

        low = CartpoleObservation(
            linear_pos=-2.5,
            linear_vel=-10.0,
            pivot_pos=-jnp.pi,
            pivot_vel=-4 * jnp.pi,
        )

        high = CartpoleObservation(
            linear_pos=2.5,
            linear_vel=10.0,
            pivot_pos=jnp.pi,
            pivot_vel=4 * jnp.pi,
        )

        return Box(low=low, high=high)

    def initial_distribution(self, state: EnvironmentState) -> Box:

        low = CartpoleObservation(
            linear_pos=-0.5,
            linear_vel=-0.5,
            pivot_pos=-jnp.pi,
            pivot_vel=-2 * jnp.pi,
        )

        high = CartpoleObservation(
            linear_pos=0.5,
            linear_vel=0.5,
            pivot_pos=jnp.pi,
            pivot_vel=2 * jnp.pi,
        )

        return Box(low=low, high=high)

    def get_observation(self, state: EnvironmentState) -> Observation:

        model = state.simulator.get_model(model_name="cartpole")

        linear_pos, pivot_pos = model.joint_positions()
        linear_vel, pivot_vel = model.joint_velocities()

        return CartpoleObservation(
            linear_pos=linear_pos,
            linear_vel=linear_vel,
            # Make sure that the pivot position is always in [-π, π]
            pivot_pos=jnp.arctan2(jnp.sin(pivot_pos), jnp.cos(pivot_pos)),
            pivot_vel=pivot_vel,
        )

    def reset(
        self, state: EnvironmentState, **kwargs
    ) -> Tuple[EnvironmentState, Observation]:

        initial_distribution = self.initial_distribution(state=state)

        subkey, state = state.generate_key()
        observation: CartpoleObservation = initial_distribution.sample(key=subkey)

        with state.editable(validate=True) as state:

            model = state.simulator.get_model(model_name="cartpole")
            model.zero()

            model.reset_joint_positions(
                positions=jnp.array([observation.linear_pos, observation.pivot_pos])
            )
            model.reset_joint_velocities(
                velocities=jnp.array([observation.linear_vel, observation.pivot_vel])
            )

        return state, self.get_observation(state)

    def step(
        self, action: Action, state: EnvironmentState
    ) -> Tuple[EnvironmentState, Tuple[Observation, Reward, IsDone, Info]]:

        with state.editable() as state:

            model = state.simulator.get_model(model_name="cartpole")

            model.zero_input()
            model.set_joint_generalized_force_targets(
                forces=action, joint_names=["linear"]
            )

            state.simulator.step()

        observation: CartpoleObservation = self.get_observation(state=state)

        is_done = jax.lax.select(
            pred=self.observation_space.contains(x=observation),
            on_true=False,
            on_false=True,
        )

        reward_alive = 1.0 - jnp.array(is_done, dtype=int)
        reward_pivot = jnp.cos(observation.pivot_pos)
        cost_action = jnp.sqrt(action.dot(action))
        cost_pivot_vel = jnp.sqrt(observation.pivot_vel**2)
        cost_linear_pos = jnp.abs(observation.linear_pos)

        reward = 0
        reward += reward_alive
        reward += reward_pivot
        reward -= 0.001 * cost_action
        reward -= 0.100 * cost_pivot_vel
        reward -= 0.500 * cost_linear_pos

        return state, (observation, reward, is_done, FrozenDict())
