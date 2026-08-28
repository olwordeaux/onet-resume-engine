# 1. Business Understanding

## Problem

A resume contains experience from different industries. The project uses O*NET data to translate that experience into consistent occupational skills, knowledge, software, tasks, and possible career transitions.

## Objective

Build a repeatable pipeline that can:

- Map resume positions to O*NET-SOC occupation codes.
- Create standardized profiles from O*NET data.
- Compare occupations using measurable overlap and similarity.
- Generate Markdown reports and composite profiles for resume analysis.

## Current Scope

The dataset contains nine selected occupations, including the four-code Independent IT Consultant and Fractional CIO composite and occupation `41-3091.00` for the inside sales role.

## Success Criteria

- Every selected occupation has the required O*NET source reports.
- Each occupation has one normalized JSON profile.
- Tidy CSV datasets can be rebuilt from the normalized profiles.
- Analysis results are reproducible from scripts.
- Tests detect missing resume data and pipeline regressions.
