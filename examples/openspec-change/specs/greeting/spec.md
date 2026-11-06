# Spec Delta

## Purpose

The greeting capability decides which name the script addresses and what it prints.

## ADDED Requirements

### Requirement: Greeting name selection

The script SHALL greet the name supplied with `--name`, and SHALL print the
default greeting when the argument is absent.

#### Scenario: Explicit name

- **WHEN** the script runs with `--name Ada`
- **THEN** it prints `Hello from Ada!`

#### Scenario: Default greeting is preserved

- **WHEN** the script runs without `--name`
- **THEN** it prints the same greeting it printed before the argument existed
