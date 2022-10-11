#!/bin/bash

serial=$(lshw -json | grep "serial: ")

echo "$serial"
