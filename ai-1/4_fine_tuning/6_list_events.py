from openai import OpenAI
client = OpenAI()

# 모든 파인 튜닝 작업 목록 가져오기
fine_tunes = client.fine_tuning.jobs.list()

for fine_tune in fine_tunes.data:
  if fine_tune.status == "running":
    print(f'running fine-tuning job: {fine_tune.id}')
    fine_tuning_running_job_id = fine_tune.id

response = client.fine_tuning.jobs.list_events(
  fine_tuning_job_id=fine_tuning_running_job_id,
  limit=2
)

print(response)
