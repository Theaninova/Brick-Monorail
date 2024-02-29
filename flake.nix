{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};
      packages =
        (with pkgs; [
          nodejs_18
          nodePackages.pnpm
        ]);
    in {
      devShell = pkgs.mkShell {
        buildInputs = packages;
      };
    });
}
