#!/bin/bash
cd /d/yj_projects/workspace_yj/Arctic/arctic_explore
while pgrep -f p3_fetch_geom.py >/dev/null; do sleep 15; done
python3 scratch/P3/p3_cellacq.py
