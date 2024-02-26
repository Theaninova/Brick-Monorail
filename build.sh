#!/usr/bin/env bash
rm -rf build
mkdir -p build
rm -rf assets/generated
mkdir -p assets/generated
jq -r '.parameterSets | keys[]' track.json | while read -r preset; do
	echo "Rendering $preset"
	openscad -o "build/$preset.stl" -p track.json -P "$preset" track.scad
	openscad -o "assets/generated/$preset.png" --imgsize=48,48 --render --autocenter --viewall -p track.json -P "$preset" track.scad
done
