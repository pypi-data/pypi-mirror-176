# Import our newly installed setuptools package.
import setuptools

# Function that takes several arguments. It assigns these values to our package.
setuptools.setup(
    # Distribution name the package. Name must be unique so adding your username at the end is common.
    name="ca_scribner_example_package",
    # Version number of your package. Semantic versioning is commonly used.
    version="0.0.3",
    # Author name.
    author="Andrew Scribner",
    # Author's email address.
    author_email="ca-scribner@gmail.com",
    # Short description that will show on the PyPi page.
    description="A dummy package",
    # Long description that will display on the PyPi page. Uses the repo's README.md to populate this.
    long_description="Package used when I need to bump a version on a dependency to test something",
    # Finds all packages within in the project and combines them into the distribution together.
    packages=setuptools.find_packages(),
    # requirements or dependencies that will be installed alongside your package when the user installs it via pip.
    # install_requires=requirements,
    # Gives pip some metadata about the package. Also displays on the PyPi page.
)
