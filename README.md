# find_a_job
This is a scraper which look for jobs vacancies on 'telegram channels'.
It will not collect vacancies containing any 'stop phrase'.
After run, it will send a .csv file with all yesterday's 'without stop phrsases' vacancies to the Telegram group.

## 1. You should create a setup file named 'andrei_jobs.json'.

The example:

{
  "profile name": "andrei_jobs",
  "min text length": 100,
  "stop phrases": [
    "middle",
    "senior",
    "lead ",
    "years of experience",
  ],
  "telegram channels": [
    "@qa_jobs",
    "@it_vacancyN1",
    "@theyseeku",
    "@jobGeeks",
    "@javadevjob",
    "@forallqa",
    "@jobforjunior",
    "@qaload_job",
  ]
}

## 2. Also, you should create a file 'private_info.json' with the data for Telegram:

The example:

{
  "api_id": "168766680",
  "api_hash": "492488a76887bf3a8721509eecd0a03",
  "phone": "+38200000000",
  "username": "User",
  "bot_token": "5502356518:AAFmHJ6thdYqlCToVaOpkvzQIsoy",
  "group_id": "-10098736549"
}
