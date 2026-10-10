{
  description = "Python dev";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs =
    {
      nixpkgs,
      ...
    }:
    let
      system = "x86_64-linux";

      pkgs = import nixpkgs { inherit system; };
      pythonPkgs = pkgs.python3Packages;
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pythonPkgs; [
          python
          flask
          requests
          venvShellHook
          python-dotenv
          unidecode
          pkgs.zuban
        ];
        venvDir = "./.venv";
      };
    };
}
