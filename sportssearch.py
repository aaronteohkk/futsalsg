from edisffo import get_offside_availability
from noiz import get_zionsports_availability
from novak import get_kovansports_availability
from egacgnallak import get_kallangcage_availability
from time import time
import multiprocessing as mp
from datetime import datetime, timedelta
from pytz import timezone
import sys


if __name__ == '__main__':

    start=time()
    if len(sys.argv) == 1:
        start_time = datetime.now(timezone('Asia/Singapore')).replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        end_time = datetime.now(timezone('Asia/Singapore')).replace(minute=0, second=0, microsecond=0) + timedelta(hours=2)
        check_date = start_time.strftime("%Y-%m-%d")
        check_time_start = start_time.strftime("%R")
        check_time_end = end_time.strftime("%R")

    else:
        check_date = sys.argv[1]
        check_time_start = sys.argv[2]
        check_time_end = sys.argv[3]

    concurrent_processes = mp.cpu_count()
    pool = mp.Pool(processes=concurrent_processes)
    offside = pool.apply_async(get_offside_availability, args=(check_date, check_time_start, check_time_end))
    kovan = pool.apply_async(get_kovansports_availability, args=(check_date, check_time_start, check_time_end))
    zion = pool.apply_async(get_zionsports_availability, args=(check_date, check_time_start, check_time_end))
    kallang = pool.apply_async(get_kallangcage_availability, args=(check_date, check_time_start, check_time_end))

    pool.close()
    pool.join()

    final= offside.get() + kovan.get() + zion.get() + kallang.get()

# offside = get_offside_availability(check_date, check_time_start, check_time_end)
# kovan = get_kovansports_availability(check_date, check_time_start, check_time_end)
# zion = get_zionsports_availability(check_date, check_time_start, check_time_end)
# final = offside + kovan + zion

    for i in sorted(final):
        print i
    if final == []:
        print 'No available pitches found.'

    print '%.2f sec.' %(time()-start)