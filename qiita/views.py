# -*- coding: utf-8 -*-
from qiita.yuba_analyze import recommend_Qiita


def recommend_QiitaProcess(daily):
    report = daily.report_y + daily.report_w + daily.report_t
    return recommend_Qiita(report)
