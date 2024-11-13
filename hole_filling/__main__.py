"""
module: __main__

Main entry point to our module
"""

# Builtin imports
import os

# Local imports
from . import cli
from .image_preprocessor import ImagePreProcessor

from .hole_filing_lib.hole_filler import HoleFiller
from .hole_filing_lib.models import Connectivity
from .hole_filing_lib.weighting import DefaultWeightMechanism

def main() -> None:
    """Main function"""
    parser = cli.get_cli_parser()
    args = parser.parse_args()

    # Validate the connectivity
    if args.connectivity == Connectivity.FOUR.value:
        connectivity = Connectivity.FOUR
    elif args.connectivity == Connectivity.EIGHT.value:
        connectivity = Connectivity.EIGHT
    else:
        print("Error: Invalid pixel connectivity. Supports 4 and 8")
        return None
    
    # Preprocess the image and mask
    preprocessor = ImagePreProcessor.from_images(args.image_path, args.mask_path)
    processed_img = preprocessor.run()

    # Create an instance of the weighting mechanism
    weighting = DefaultWeightMechanism(args.z, args.e)

    # Compute the output path
    output_directory = args.output_directory
    if not output_directory:
        output_directory = os.path.dirname(args.image_path)

    filler = HoleFiller(processed_img,
                        weighting=weighting,
                        connectivity=connectivity,
                        output_directory=output_directory,
                        debug=args.debug)
    filler.fill()

if __name__ == "__main__":
    main()
