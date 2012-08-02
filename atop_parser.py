#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import tempfile

class atopStore(object):

  __common_fieldnames = ["label", "host", "epoch", "date", "time", "interval"]

  CPU_fieldnames = __common_fieldnames + ["ticks_per_second", "number_of_processors", "system", "user", "nice", "idle", "wait", "irq", "sirq", "steal", "guest", "unknown1", "unknown2"]

  cpu_fieldnames = __common_fieldnames + ["ticks_per_second", "processor_number", "system", "user", "nice", "idle", "wait", "irq", "sirq", "steal", "guest", "unknown1", "unknown2"]

  CPL_fieldnames = __common_fieldnames + ["number_of_processors", "last_minute", "last_five_minutes", "last_fifteen_minutes", "number_of_context_switches", "number_of_interrupts"]

  MEM_fieldnames = __common_fieldnames + ["page_size", "size_of_physical_memory", "size_of_free_memory", "size_of_page_cache", "size_of_buffer_cache", "size_of_slab", "number_of_dirty_pages"]

  SWP_fieldnames = __common_fieldnames + ["page_size", "size_of_swap", "size_of_free_swap", "0", "size_of_committed_space", "limit_for_committed_space"]

  PAG_fieldnames = __common_fieldnames + ["page_size", "number_of_page_scans", "number_of_allocstalls", "0", "number_of_swapins", "number_of_swapouts"]

  LVM_fieldnames = __common_fieldnames + ["name", "number_of_milliseconds_spent_for_I/O", "number_of_reads_issued", "number_of_sectors_transferred_for_reads", "number_of_writes_issued", "number_of_sectors_transferred_for_write"]

  MDD_fieldnames = LVM_fieldnames

  DSK_fieldnames = LVM_fieldnames

  NET_upper_fieldnames = __common_fieldnames + ["name", "number_of_packets_received_by_TCP", "number_of_packets_transmitted_by_TCP", "number_of_packets_received_by_UDP", "number_of_packets_transmitted_by_UDP", "number_of_packets_received_by_IP", "number_of_packets_transmitted_by_IP", "number_of_packets_delivered", "number_of_packets_forwarded"]

  NET_fieldnames = __common_fieldnames + ["name", "number_of_packets_received", "number_of_bytes_received", "number_of_packets_transmitted", "number_of_bytes_transmitted", "speed", "duplex_mode"]

  PRG_fieldnames = __common_fieldnames + ["PID", "name", "state", "real_uid", "real_gid", "TGID", "total_number_of_threads", "exit_code", "start_time", "full_command_line", "PPID", "number_of_threads_in_state_'running'", "number_of_threads_in_state_'interruptible_sleeping'", "number_of_threads_in_state_'uninterruptible_sleeping'", "effective_uid", "effective_gid", "saved_uid", "saved_gid", "filesystem_uid", "filesystem_gid", "elapsed time"]

  PRC_fieldnames = __common_fieldnames + ["PID", "name", "state", "ticks_per_second", "user", "system", "nice_value", "priority", "realtime_priority", "scheduling_policy", "current_CPU", "sleep_average"]

  PRM_fieldnames = __common_fieldnames + ["PID", "name", "state", "page_size", "virtual_memory_size", "resident_memory_size", "shared_text_memory_size", "virtual_memory_growth", "resident_memory_growth", "number_of_minor_page_faults", "number_of_major_page_faults"]

  PRD_fieldnames = __common_fieldnames + ["PID", "name", "state", "kernel-patch_installed", "standard_io_statistics_used", "number_of_reads", "cumulative_number_of_sectors_read", "number_of_writes_on_disk", "cumulative_number_of_sectors_written", "cancelled_number_of_written_sectors"]

  PRN_fieldnames = __common_fieldnames + ["PID", "name", "state", "kernel-patch_installed", "number_of_TCP-packets_transmitted", "cumulative_size_of_TCP-packets_transmitted", "number_of_TCP-packets_received", "cumulative_size_of_TCP-packets_received", "number_of_UDP-packets_transmitted", "cumulative_size_of_UDP-packets_transmitted", "number_of_UDP-packets_received", "cumulative_size_of_UDP-packets_transmitted", "number_of_raw_packets_transmitted", "number_of_raw_packets_received"]

  def __init__(self, filename, delimiter=' '):
    self.filename = filename
    self.delimiter = delimiter

  def __getattr__(self, attr_name):
    func = attr_name.split('_')
    if "series" != func[0] or 2 != len(func):
      return object.__getattribute__(self, attr_name)

    names = {}
    items = {}

    s = open(self.filename, "r").read().replace("(", "\"").replace(")", "\"")

    f = tempfile.NamedTemporaryFile()
    f.write(s)
    f.flush()

    data = csv.reader(open(f.name, "r"), quotechar="\"", delimiter=self.delimiter)
    for row in data:
      label = row[0]
      if "SEP" == label or "RESET" == label or func[1] != label:
        continue

      if label in ["LVM", "MDD", "DSK", "NET", "PRG", "PRC", "PRM", "PRD", "PRN"]:
        if row[6] not in names:
          names[row[6]] = {}
          items = names
        container = names[row[6]]
        field_index = 7
      elif label in ["cpu"]:
        if row[7] not in names:
          names[row[7]] = {}
          items = names
        container = names[row[7]]
        field_index = 8
      else:
        container = items
        field_index = 6

      if "NET" == label:
        dev = row[6]
        if "upper" == dev:
          fields = atopStore.__dict__["NET_upper_fieldnames"]
        else:
          fields = atopStore.__dict__["NET_fieldnames"]
      else:
        fields = atopStore.__dict__[label + "_fieldnames"]

      for i in [2] + range(field_index, len(row)):
        key = fields[i]
        series = container.setdefault(key, [])
        series.append(row[i])
    return items

if __name__ == "__main__":
  store = atopStore("20120709ALL.txt")
  print store.series_PRC

