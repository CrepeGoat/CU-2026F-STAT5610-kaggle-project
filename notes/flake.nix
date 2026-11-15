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
        in
        {
          default = pkgs.mkShell {
            buildInputs = with pkgs; [
              pandoc
            ];
          };
        }
      );
    };
}
