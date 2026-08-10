#!/bin/bash
systemctl is-active --quiet hermes-richard.service || systemctl restart hermes-richard.service
