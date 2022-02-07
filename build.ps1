python -m build
pip wheel . -w wheels
$wheels = Get-ChildItem -Path .\wheels\ -Name
pip install .\wheels\$wheels --force-reinstall

python -m twine upload --repository testpypi dist/*