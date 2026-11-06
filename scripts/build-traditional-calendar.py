#!/usr/bin/env python3
"""Build the supplemental and combined calendars from checked-in date data."""
import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data' / 'traditional-calendar.json'
STAMP = '20261106T000000Z'
SOURCE = 'https://www.hko.gov.hk/sc/gts/time/conversion1_text.htm'
PMO_SOURCE = 'https://www.pmo.cas.cn/xwdt2019/kpdt2019/202203/P020251230620718707826.pdf'
PMO_TERMS = {2026: {1, 2, 3, 7, 8, 9, 10, 11, 12}, 2027: {1, 2}}


def fold(line):
    """Fold UTF-8 iCalendar lines at 75 octets without splitting characters."""
    chunks, current = [], ''
    for char in line:
        if len((current + char).encode('utf-8')) > 75:
            chunks.append(current)
            current = ' ' + char
        else:
            current += char
    chunks.append(current)
    return '\r\n'.join(chunks)


def event(date, name, kind):
    d = datetime.date.fromisoformat(date)
    next_day = d + datetime.timedelta(days=1)
    key = 'festival' if kind == '传统节日' else 'solar-term'
    uid = f'{d:%Y%m%d}-{key}-{name}@samsurtee-china-holidays'
    source = (PMO_SOURCE if kind == '节气' and d.month in PMO_TERMS.get(d.year, set()) else SOURCE)
    return [
        'BEGIN:VEVENT', f'DTSTART;VALUE=DATE:{d:%Y%m%d}',
        f'DTEND;VALUE=DATE:{next_day:%Y%m%d}', f'DTSTAMP:{STAMP}',
        f'UID:{uid}', f'SUMMARY:{name}（{kind}）',
        f'DESCRIPTION:{kind}日期。数据来源：' + ('中国科学院紫金山天文台' if source == PMO_SOURCE else '香港天文台') + f'\\n{source}',
        'TRANSP:TRANSPARENT', 'END:VEVENT',
    ]


def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    records = []
    for year, contents in data.items():
        for key, kind in [('festivals', '传统节日'), ('solar_terms', '节气')]:
            for item in contents[key]:
                assert item['date'].startswith(year + '-')
                records.append((item['date'], item['name'], kind))
    assert len(records) == len(set(records)), 'Duplicate events'
    body = [line for date, name, kind in sorted(records) for line in event(date, name, kind)]
    header = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//SamsurTee//Traditional Calendar//CN',
              'CALSCALE:GREGORIAN', 'METHOD:PUBLISH', 'X-WR-CALNAME:中国传统节日和二十四节气',
              'X-WR-TIMEZONE:Asia/Shanghai']
    supplemental = '\r\n'.join(map(fold, header + body + ['END:VCALENDAR'])) + '\r\n'
    (ROOT / 'traditionalCalendar.ics').write_bytes(supplemental.encode('utf-8'))
    base = (ROOT / 'holidayCal.ics').read_text(encoding='utf-8').splitlines()
    assert base[-1] == 'END:VCALENDAR'
    base = [('X-WR-CALNAME:中国节假日、补班、传统节日和节气' if line.startswith('X-WR-CALNAME:') else line) for line in base[:-1]]
    combined = '\r\n'.join(base + [fold(line) for line in body] + ['END:VCALENDAR']) + '\r\n'
    (ROOT / 'completeCalendar.ics').write_bytes(combined.encode('utf-8'))
    print(f'Generated {len(records)} traditional festival and solar term events.')


if __name__ == '__main__':
    main()
