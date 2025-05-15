To use CICFlowMeter, please create the docker container using the instructions provided here: https://github.com/ahlashkari/CICFlowMeter/issues/155

You can use the following command to process the data:
```bash
docker run -v <pcap_flows_folder>:/tmp/server_ndt -v <output_folder>:/tmp/output/ --entrypoint /bin/bash --rm cicflowmeter:latest -c "find /tmp/server_ndt -maxdepth 1 -type f -name '*.pcap' | parallel java -Djava.library.path=/CICFlowMeter/jnetpcap/linux/jnetpcap-1.4.r1425/ -jar build/libs/CICFlowMeter-4.0.jar {} /tmp/output/"
```


Or if you have a folder with subfolders:
```bash
docker run -v <pcap_flows_folder_with_subfolders>:/tmp/server_ndt -v <output_folder>:/tmp/output/ --entrypoint /bin/bash --rm cicflowmeter:latest -c "find /tmp/server_ndt -type d -exec mkdir -p /tmp/output/{} \; && find /tmp/server_ndt -type f -name '*.pcap' | parallel 'java -Djava.library.path=/CICFlowMeter/jnetpcap/linux/jnetpcap-1.4.r1425/ -jar build/libs/CICFlowMeter-4.0.jar {} /tmp/output/{//}/'"
```

After this, use merger.py to merge all the small CSV files into one file:

```bash
python3 merger.py <output_folder> <result_name>.csv
```