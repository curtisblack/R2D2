#!/usr/bin/env bash

echo "#!/usr/bin/env bash" > /usr/local/bin/run
echo "python /home/pi/R2D2/run.py \"\$@\"" >> /usr/local/bin/run
chmod 755 /usr/local/bin/run
