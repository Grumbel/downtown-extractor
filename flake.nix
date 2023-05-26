{
  description = "File extractor for the game Goin' Downtown";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonPackages = pkgs.python310Packages;
      in rec {
        packages = rec {
          default = downtown-extractor;

          downtown-extractor = pythonPackages.buildPythonPackage rec {
            name = "downtown-extractor";
            version = "0.1.0";

            src = ./.;

            doCheck = true;

            checkPhase = ''
              runHook preCheck
              flake8 --max-line-length 120 downtown_extractor.py
              mypy --strict downtown_extractor.py
              pylint downtown_extractor.py
              runHook postCheck
            '';

            nativeCheckInputs = with pythonPackages; [
              flake8
              mypy
              pylint
              types-setuptools
              pip
            ];

            propagatedBuildInputs = with pythonPackages; [
              setuptools
            ];
          };
        };

        apps = rec {
          default = downtown-extractor;

          downtown-extractor = flake-utils.lib.mkApp {
            drv = packages.downtown-extractor;
            exePath = "/bin/downtown-extractor";
          };
        };
      }
    );
}
