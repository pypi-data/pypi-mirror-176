from omegaconf import DictConfig
from vehiclemodels.vehicle_parameters import setup_vehicle_parameters


def parameters_vehicle3() -> DictConfig:
    """
    Creates an OmegaConf DictConfig object holding all vehicle parameters for vehicle ID 3 (VW Vanagon)
    """
    return setup_vehicle_parameters(vehicle_id=3)


# Test parameters
if __name__ == "__main__":
    params = parameters_vehicle3()
