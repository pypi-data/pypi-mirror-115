# redfish_advantech

## Build package
- cd to the directory of setup.py
- Confirm the version number in setup.py and src/redfish_advantech/__init__.py

python setup.py sdist build
twine upload dist/*

## Uninstall the redfish_advantech
pip uninstall redfish_advantech -y

## Install the redfish_advantech
pip install redfish_advantech

or

pip install redfish_advantech==x.y.z
- where the x.y.z is the version number

## Test (Change to the directory which has logging.conf)
- Make sure the python is version 3.x
- Make sure the logging.conf is exist in the same directory as test sample code
- Add "-v", "-vv" or "-vvv" for more log

cd examples
python advantech.py
python acl_bmc.py
python acl_bmc_cm.py

