import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')

# 1. Update Follow-ups & Active Trials with explicit Origin Column
ws_fol = sh.worksheet('🔄 Follow-ups & Active Trials')

today = '2026-09-02'
warm_leads = [
    [
        '🔥 Warm Reply (Inbound)',
        '🏢 Company Routed',
        'Vilca - Venezuelan International Logistic, C.A.',
        'Venezuela (Caracas)',
        'Juan Miguel Polese',
        'General Manager',
        'juan.polese@vilca.biz',
        'https://www.vilca.biz',
        'Tracking API (150 containers/mo + Air AWB)',
        '🏢 Company Outbound (Routed by Ekaterina)',
        'Nikita Kurudzhy',
        today,
        today,
        '2026-09-04',
        'Current provider too expensive. Needs cost improvement. Expects ~150 ocean containers + Air AWBs. Sent trackingmcp.com/auth/signup trial link + pricing framework.',
        'Wait for registration email or call confirmation for Friday.'
    ],
    [
        '🔥 Warm Reply (Inbound)',
        '🏢 Company Routed',
        'Sattva Global Logistics',
        'India',
        'Sujith Nair',
        'Logistics & IT Lead',
        'sujith@sattvaglobal.in',
        'https://sattvaglobal.in',
        'Tracking API (25 shipments/mo) + Schedules API',
        '🏢 Company Outbound (Routed by Ekaterina)',
        'Nikita Kurudzhy',
        today,
        today,
        '2026-09-04',
        'Leaving ShipsGo due to mandatory annual lock-in. Volume ~25 shipments/mo. Prefers email only. Offered $50/mo plan (750 calls), sent docs and trackingmcp.com/auth/signup trial link.',
        'Wait for account creation email to activate trial access.'
    ]
]

headers_fol = [
    'Lead Status (Статус лида)',
    'Lead Origin (Источник/Категория)',
    'Company Name (Компания)',
    'Country (Страна)',
    'Contact Person (ЛПР)',
    'Job Title (Должность)',
    'Email (Personal ЛПР)',
    'Website / LinkedIn',
    'Product Interest (Интерес к продукту)',
    'Source Channel (Детали источника)',
    'Assigned AE (Ответственный)',
    'First Touch Date',
    'Last Interaction Date',
    'Next Follow-up Date (Дата следующего шага)',
    'Stage Details / Commercial Notes (История и детали сделки)',
    'Next Step Action (Следующее действие)'
]

ws_fol.clear()
ws_fol.update(values=[headers_fol] + warm_leads, range_name=f'A1:P{len(warm_leads)+1}', value_input_option='USER_ENTERED')
print("Follow-ups tab updated with explicit Lead Origin & Assigned AE!")

# 2. Update Monthly Dashboard to split Personal Nikita Outreach vs Company Inbound
ws_dash = sh.worksheet('📊 Monthly Dashboard')

dash_structure = [
    ['NAVO24: РАЗДЕЛЬНЫЙ ДАШБОРД ПРОДАЖ И КОНВЕРСИЙ (NIKITA PIPELINE vs COMPANY INBOUND)', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
    ['', '👤 NIKITA PERSONAL EMAIL OUTREACH', '', '', '', '', '👤 NIKITA LINKEDIN OUTREACH', '', '', '', '', '🏢 COMPANY ROUTED LEADS', '', '', 'TOTALS', ''],
    ['Месяц (Month)', 'Base', 'Sent', 'Replied', 'Reply %', 'Trials', 'Base', 'Sent', 'Replied', 'Reply %', 'Trials', 'Routed Leads', 'Active Trials', 'Conversion %', 'Total Trials', 'Closed Won ($)'],
    ['September 2026', 100, 0, 0, '=IF(C5>0, D5/C5, 0)', 0, 34, 0, 0, '=IF(H5>0, I5/H5, 0)', 0, 2, 2, '=IF(L5>0, M5/L5, 0)', '=F5+K5+M5', '$0'],
    ['October 2026', 0, 0, 0, '=IF(C6>0, D6/C6, 0)', 0, 0, 0, 0, '=IF(H6>0, I6/H6, 0)', 0, 0, 0, '=IF(L6>0, M6/L6, 0)', '=F6+K6+M6', '$0'],
    ['November 2026', 0, 0, 0, '=IF(C7>0, D7/C7, 0)', 0, 0, 0, 0, '=IF(H7>0, I7/H7, 0)', 0, 0, 0, '=IF(L7>0, M7/L7, 0)', '=F7+K7+M7', '$0'],
    ['December 2026', 0, 0, 0, '=IF(C8>0, D8/C8, 0)', 0, 0, 0, 0, '=IF(H8>0, I8/H8, 0)', 0, 0, 0, '=IF(L8>0, M8/L8, 0)', '=F8+K8+M8', '$0'],
    ['January 2027', 0, 0, 0, '=IF(C9>0, D9/C9, 0)', 0, 0, 0, 0, '=IF(H9>0, I9/H9, 0)', 0, 0, 0, '=IF(L9>0, M9/L9, 0)', '=F9+K9+M9', '$0'],
    ['ИТОГО / TOTAL', '=SUM(B5:B9)', '=SUM(C5:C9)', '=SUM(D5:D9)', '=IF(C10>0, D10/C10, 0)', '=SUM(F5:F9)', '=SUM(G5:G9)', '=SUM(H5:H9)', '=SUM(I5:I9)', '=IF(H10>0, I10/H10, 0)', '=SUM(K5:K9)', '=SUM(L5:L9)', '=SUM(M5:M9)', '=IF(L10>0, M10/L10, 0)', '=SUM(O5:O9)', '=SUM(P5:P9)']
]

ws_dash.clear()
ws_dash.update(values=dash_structure, range_name=f'A1:P{len(dash_structure)}', value_input_option='USER_ENTERED')
print("Monthly Dashboard successfully split into Personal vs Company channels!")
