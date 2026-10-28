# 10/17 이슈 게시 전 확인(읽기·작은 실험만): torch.cuda.Stream() 이 매번 새 스트림을 만드는지, 32개 풀에서 돌려 쓰는지,
# 그리고 스트림마다 캐시 블록이 따로 남아 예약 메모리가 늘어나는지(모델 없이 작은 텐서로 재현).
import torch
ids = [torch.cuda.Stream().cuda_stream for _ in range(80)]
print("distinct stream handles over 80 calls:", len(set(ids)))
torch.cuda.empty_cache(); base = torch.cuda.memory_reserved()
x = torch.randn(1024, 1024, device="cuda")
for k in range(40):
    s = torch.cuda.Stream()
    with torch.cuda.stream(s):
        y = (x @ x).relu_()          # 4 MB 결과 + 임시 블록을 이 스트림에서 할당
    torch.cuda.synchronize(); del y
    if k in (0, 1, 3, 7, 15, 31, 39): print(f"after {k + 1:2d} calls: reserved +{(torch.cuda.memory_reserved() - base) / 2**20:.0f} MiB")
torch.cuda.empty_cache(); base = torch.cuda.memory_reserved()
for k in range(40):
    y = (x @ x).relu_(); torch.cuda.synchronize(); del y
print(f"default stream, 40 calls: reserved +{(torch.cuda.memory_reserved() - base) / 2**20:.0f} MiB")
