import os, datetime

date_format = '%Y%m%d%H%M'
pools = ["<pools>"]
snapshot_prefix = 'pysnap'

# Get todays date for the new snapshot
current_date = datetime.datetime.now()

# Get yesterdays date for removing the old snapshot
previous_date = current_date - datetime.timedelta(days=2)

for pool in pools:
    # List existing snapshots of the specified pool
    command = '/usr/sbin/zfs list -t snapshot | grep {}'.format(pool)
    print('Finding existing snapshots: $ {}'.format(command))
    output = os.popen(command)
    snapshots = output.readlines()

    # Create the new snapshot
    command = '/usr/sbin/zfs snapshot -r {}@{}{}'.format(pool, snapshot_prefix, current_date.strftime(date_format))
    print('Creating new snapshot: $ {}'.format(command))
    os.system(command)

    # Determine if the previous snapshot even exists before deleting it
    for line in snapshots:
        if (line.find('{}@{}{}'.format(pool, snapshot_prefix, previous_date.strftime(date_format)[0:8])) != -1):
            # Get the old snapshot name
            old_snapshot = line[0:line.find(' ')]
            # Delete the old snapshot
            command = '/usr/sbin/zfs destroy -r {}'.format(old_snapshot)
            print('Deleting old snapshot: $ {}'.format(command))
            os.system(command)
