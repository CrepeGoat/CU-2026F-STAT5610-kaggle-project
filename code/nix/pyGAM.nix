# https://nixos.org/manual/nixpkgs/stable/#python
# https://github.com/NixOS/nixpkgs/blob/master/doc/languages-frameworks/python.section.md

{
  lib,
  buildPythonPackage,
  fetchPypi,
  pytestCheckHook,
  pythonRelaxDepsHook,
  setuptools,
  numpy,
  pandas,
  scipy,
  progressbar2,
}:

buildPythonPackage rec {
  pname = "pyGAM";
  version = "0.12.0";
  pyproject = true;

  src = fetchPypi {
    inherit version;
    pname = "pygam";
    hash = "sha256-fAmN+/u3prn6ThpXk4DjsLhm/o+lb52FL/3q7P5W1eo=";
  };

  build-system = [ setuptools ];

  nativeCheckInputs = [
    # pytestCheckHook # https://nixos.org/manual/nixpkgs/stable/#using-pytestcheckhook
  ];

  pythonRelaxDeps = [ "scipy" ];

  dependencies = [
    numpy
    pandas
    scipy
    progressbar2
  ];

  pythonImportsCheck = [ "pygam" ];

  meta = {
    description = "Generalized Additive Models in Python.";
    homepage = "https://github.com/dswah/pyGAM";
    license = lib.licenses.asl20;
  };
}
