from omegaconf import DictConfig
from vehiclemodels.vehicle_parameters import setup_vehicle_parameters


def parameters_vehicle4() -> DictConfig:
    """
    Creates an OmegaConf DictConfig object holding all vehicle parameters vehicle ID 4 (semi-trailer truck)
    """
    return setup_vehicle_parameters(vehicle_id=4)


# Test parameters
if __name__ == "__main__":
    params = parameters_vehicle4()
