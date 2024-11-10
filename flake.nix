{
  nixConfig = {
    extra-experimental-features = "nix-command flakes";
    extra-substituters = "https://marcus7070.cachix.org";
    extra-trusted-public-keys = "marcus7070.cachix.org-1:JawxHSgnYsgNYJmNqZwvLjI4NcOwrcEZDToWlT3WwXw=";
  };
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    cadquery.url = "github:vinszent/cq-flake";
  };
  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      cadquery,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ (final: prev: { cadquery = cadquery.packages.${system}; }) ];
        };
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = [
            pkgs.cadquery.python
            pkgs.cadquery.cadquery
            pkgs.cadquery.cq-editor
          ];
        };
      }
    );
}
