# 中国节假日补班日历

本项目是 [lanceliao/china-holiday-calender](https://github.com/lanceliao/china-holiday-calender) 的个人维护版本，提供中国节假日和补班日历。当前数据覆盖 2023—2027 年；2027 年安排依据[国务院办公厅通知](https://www.gov.cn/zhengce/content/202611/content_7085101.htm)。

## 订阅日历

在日历应用中选择“订阅日历”或“添加订阅日历”，复制以下对应链接：

- [放假和补班](https://raw.githubusercontent.com/SamsurTee/china-holiday-calender/master/holidayCal.ics)
- [仅放假](https://raw.githubusercontent.com/SamsurTee/china-holiday-calender/master/holidayCal-HO.ics)
- [仅补班](https://raw.githubusercontent.com/SamsurTee/china-holiday-calender/master/holidayCal-CO.ics)
- [传统节日和二十四节气](https://raw.githubusercontent.com/SamsurTee/china-holiday-calender/master/traditionalCalendar.ics)
- [综合日历：放假、补班、传统节日和节气](https://raw.githubusercontent.com/SamsurTee/china-holiday-calender/master/completeCalendar.ics)

传统节日和节气目前覆盖 **2026—2027 年**，按北京时间（UTC+8）以全天事件显示。维护时优先核对中国科学院紫金山天文台的历书；目前已用[紫金山天文台《2026年日历资料》](https://www.pmo.cas.cn/xwdt2019/kpdt2019/202203/P020251230620718707826.pdf)核对其中 2026 年 1—3 月、7—12 月及 2027 年 1—2 月的节气日期，其余日期依据[香港天文台公历与农历日期对照表](https://www.hko.gov.hk/sc/gts/time/conversion1_text.htm)。传统节日包括除夕、春节、元宵节、龙抬头、清明节、端午节、七夕节、中元节、中秋节、重阳节和腊八节。综合日历可能在同一天显示假期、节日或节气等多个事件；节日和节气本身不代表放假。

建议选择综合日历，或分别选择放假补班日历与传统节日日历，以避免重复订阅。

这些链接直接读取本仓库默认分支上的文件。更新文件后，订阅者会在日历应用下次刷新时收到更新；刷新频率取决于各日历应用。GitHub 在不同网络环境下的访问情况可能不同。

放假日程为全天事件，标题标明假期天数；补班日程为全天事件，不设置默认提醒。上述静态订阅地址不支持通过 URL 参数定制补班时间或提醒。

## JSON 数据

[查看 holidayAPI.json](https://raw.githubusercontent.com/SamsurTee/china-holiday-calender/master/holidayAPI.json)

数据按年份组织，每个节假日包含名称、开始和结束日期、天数、补班日期、通知链接及说明。

| 字段 | 说明 |
| --- | --- |
| Name | 节假日名称 |
| StartDate / EndDate | 假期开始和结束日期，格式为 `YYYY-MM-DD` |
| Duration | 假期天数 |
| CompDays | 补班日期数组 |
| URL | 放假通知链接 |
| Memo | 放假通知中的相关说明 |

## 维护

本仓库由维护者自行更新，fork 不会自动同步原项目。新增或修改安排时，需要同步检查 `holidayAPI.json` 和三份 `.ics` 文件，确保放假日期、补班日期与提醒一致。可依据官方通知更新，并在日历和 JSON 中保留来源链接。节气和农历日期优先查阅中国科学院紫金山天文台历书，并记录实际使用的数据出处。传统节日和节气日期保存在 `data/traditional-calendar.json`；核对并添加新年份后，运行 `python3 scripts/build-traditional-calendar.py` 重新生成单独日历和综合日历。修改 `holidayCal.ics` 后也应重新运行该命令，以同步综合日历。

## 致谢

本项目基于 [lanceliao/china-holiday-calender](https://github.com/lanceliao/china-holiday-calender)，感谢原项目作者和贡献者。
