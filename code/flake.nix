{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    {
      self,
      nixpkgs,
    }:

    let
      forEachSystem =
        makeFlakeWithSystem:
        nixpkgs.lib.genAttrs [
          "aarch64-darwin"
          "aarch64-linux"
          "x86_64-darwin"
          "x86_64-linux"
        ] makeFlakeWithSystem;
    in
    {
      devShells = forEachSystem (
        system:
        let
          pkgs = import nixpkgs { inherit system; };
          python = pkgs.python314;
          pyPkgs = pkgs.python314Packages;
          inherit (pkgs.lib) callPackageWith;
        in
        {
          default = pkgs.mkShell {
            buildInputs = [
              python
            ]
            ++ (with pyPkgs; [
              kagglehub
              python-dotenv

              jupyterlab
              ipykernel
              marimo

              numpy
              pandas
              statsmodels
              scikit-learn
              sortedcontainers

              matplotlib
              seaborn
            ])
            ++ [ (callPackageWith (pkgs // pyPkgs) ./nix/pyGAM.nix { }) ];
          };
        }
      );
    };
}
