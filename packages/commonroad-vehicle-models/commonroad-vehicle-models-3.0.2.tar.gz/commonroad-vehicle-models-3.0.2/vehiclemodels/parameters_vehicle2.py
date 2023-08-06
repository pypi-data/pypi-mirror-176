from omegaconf import DictConfig
from vehiclemodels.vehicle_parameters import setup_vehicle_parameters


def parameters_vehicle2() -> DictConfig:
    """
    Creates an OmegaConf DictConfig object holding all vehicle parameters vehicle ID 2 (BMW 320i)
    """
    return setup_vehicle_parameters(vehicle_id=2)


# Test parameters
if __name__ == "__main__":
    params = parameters_vehicle2()
