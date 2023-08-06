from pathlib import Path
from typing import Tuple, ClassVar

import jax
import jax.numpy as jnp
import jax_dataclasses

from jaxsim import high_level
from jaxsim.gym import Env, EnvironmentState
from jaxsim.gym.spaces import Box
from jaxsim.gym.typing import *
from jaxsim.simulation.simulator import JaxSim, SimulatorData
from jaxsim.utils import JaxsimDataclass


@jax_dataclasses.pytree_dataclass
class PendulumObservation(JaxsimDataclass):

    cos_theta: jtp.Float
    sin_theta: jtp.Float
    omega: jtp.Float


@jax_dataclasses.pytree_dataclass
class PendulumEnvironment(Env):

    name: ClassVar = jax_dataclasses.static_field(default="pendulum")

    @staticmethod
    def build() -> Tuple["PendulumEnvironment", EnvironmentState]:

        T = 0.050
        dt = 0.000_200

        simulator = JaxSim(
            step_size=dt,
            steps_per_run=int(T / dt),
            velocity_representation=high_level.model.VelRepr.Body,
            data=SimulatorData(gravity=jnp.array([0, 0, -10.0])),
        )

        with simulator.editable(validate=False) as simulator:

            simulator: JaxSim
            sdf_path = Path("~/git/jaxsim/examples/resources/pendulum.sdf")
            _ = simulator.insert_model_from_sdf(sdf=sdf_path.expanduser().absolute())
            # TODO: disable contacts?

        with EnvironmentState().editable(validate=False) as state:
            state.simulator = simulator

        with PendulumEnvironment(_action_space=None, _observation_space=None).editable(
            validate=False
        ) as env:

            env._action_space = env.build_action_space(state=state)
            env._observation_space = env.build_observation_space(state=state)

        return env, EnvironmentState.to_jax(state=state)

    def build_action_space(self, state: EnvironmentState) -> Box:

        return Box(low=-5.0, high=5.0)
        # return Box(low=-2.0, high=2.0)

    def build_observation_space(self, state: EnvironmentState) -> Box:

        high = PendulumObservation(cos_theta=1.0, sin_theta=1.0, omega=8.0)
        low = PendulumObservation(cos_theta=-1.0, sin_theta=-1.0, omega=-8.0)

        return Box(low=low, high=high)

    def initial_distribution(self, state: EnvironmentState) -> Box:

        high = jnp.array([jnp.pi, 1.0])
        return Box(low=-high, high=high)

    def get_observation(self, state: EnvironmentState) -> Observation:

        model = state.simulator.get_model(model_name="pendulum")

        theta = model.joint_positions()[0]
        omega = model.joint_velocities()[0]

        return PendulumObservation(
            cos_theta=jnp.cos(theta), sin_theta=jnp.sin(theta), omega=omega
        )

    def reset(
        self, state: EnvironmentState, **kwargs
    ) -> Tuple[EnvironmentState, Observation]:

        initial_distribution = self.initial_distribution(state=state)

        subkey, state = state.generate_key()
        theta, omega = initial_distribution.sample(key=subkey)

        with state.editable(validate=True) as state:

            model = state.simulator.get_model(model_name="pendulum")
            model.zero()

            model.reset_joint_positions(positions=jnp.array([theta]))
            model.reset_joint_velocities(velocities=jnp.array([omega]))

        return state, self.get_observation(state)

    def step(
        self, action: Action, state: EnvironmentState
    ) -> Tuple[EnvironmentState, Tuple[Observation, Reward, IsDone, Info]]:

        with state.editable() as state:

            model = state.simulator.get_model(model_name="pendulum")

            model.zero_input()
            model.set_joint_generalized_force_targets(
                forces=action, joint_names=["pivot"]
            )

            state.simulator.step()

        observation: PendulumObservation = self.get_observation(state=state)
        theta = jnp.arctan2(observation.sin_theta, observation.cos_theta)

        is_done = jax.lax.select(
            pred=self.observation_space.contains(x=observation),
            on_true=False,
            on_false=True,
        )

        reward = 0.0 - jnp.array(is_done, dtype=float)
        reward -= jnp.power(theta, 2)
        reward -= 0.1 * jnp.power(observation.omega, 2)
        reward -= 0.001 * jnp.sqrt(jnp.power(action, 2))

        return state, (observation, reward, is_done, FrozenDict())
