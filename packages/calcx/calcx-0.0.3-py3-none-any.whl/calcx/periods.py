APPROX_BDAYS_PER_MONTH = 21
APPROX_BDAYS_PER_YEAR = 252

MONTHS_PER_YEAR = 12
WEEKS_PER_YEAR = 52
QTRS_PER_YEAR = 4

DAILY = 'daily'
WEEKLY = 'weekly'
MONTHLY = 'monthly'
QUARTERLY = 'quarterly'
YEARLY = 'yearly'

# 近1月
PAST_MONTH = "past_month"
# 近3月
PAST_QUARTER = "past_quarter"
# 近6月
PAST_HALF_YEAR = "past_half_year"
# 近1年
PAST_YEAR = "past_year"
# 近2年
PAST_TWO_YEAR = "past_two_year"
# 近3年
PAST_THREE_YEAR = "past_three_year"
# 今年以来
THIS_YEAR = "this_year"
# -----------------------
# 本月
THIS_MONTH = "this_month"
# 本季
THIS_QUARTER = "this_quarter"
# 近5年
PAST_FIVE_YEAR = "past_five_year"

ANNUALIZATION_FACTORS = {
    DAILY: APPROX_BDAYS_PER_YEAR,
    WEEKLY: WEEKS_PER_YEAR,
    MONTHLY: MONTHS_PER_YEAR,
    QUARTERLY: QTRS_PER_YEAR,
    YEARLY: 1
}
