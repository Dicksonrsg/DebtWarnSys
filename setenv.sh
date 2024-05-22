#!/bin/sh
export $(cat .env | xargs -L 1)