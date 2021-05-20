def radarfetch(file_name, save_path):
    import radarclient
    import pandas as pd
    import os
    from datetime import datetime
    system_identifier = radarclient.ClientSystemIdentifier('ICTJS', '1.0')
    radar_client = radarclient.RadarClient(
        radarclient.AuthenticationStrategySPNego(), system_identifier)
    udf = pd.read_excel(file_name)
    total_radars = int(udf.size / 3)
    n = 0
    time_zero = datetime.now()
    print("0 out of {} radars completed, estimated completed time: calculating.".format(total_radars))
    for i in udf.iterrows():
        SN = i[1][0]
        radar_num = i[1][1]
        waterfall_id = i[1][2]
        radar = radar_client.radar_for_id(radar_num)
        attc = radar.attachment_archive_download_enclosure()
        save_to = "{}/waterfall{}/{}/{}".format(
            save_path, waterfall_id, SN, attc.file_name)
        dirname = os.path.dirname(save_to)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(save_to, 'wb') as f:
            attc.write_to_file(f)
        n += 1
        time_used = datetime.now() - time_zero
        time_end = datetime.now() + time_used * (total_radars - n) / n
        print("{} out of {} radars completed, estimated completed time:{}.".format(
            n, total_radars, time_end.strftime("%Y-%m-%d %H:%M")))

import sys

if __name__ == '__main__':
    fn = input("Please enter the xls filename and path:")
    sp = input("Please enter the path of the saved radar attachments:")
    radarfetch(fn, sp)
