
# anaconda(또는 miniconda)가 존재하지 않을 경우 설치해주세요!
## TODO
if ! command -v conda &> /dev/null; then
    echo "[INFO] conda 없음. Miniconda 설치 시작"
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -p "$HOME/miniconda"
    export PATH="$HOME/miniconda/bin:$PATH"
fi
source "$(conda info --base)/etc/profile.d/conda.sh"

# Conda 환경 생성 및 활성화
## TODO
ENV_NAME="myenv"
conda create --name "$ENV_NAME" python=3.12 -y
conda activate myenv

## 건드리지 마세요! ##
python_env=$(python -c "import sys; print(sys.prefix)")
if [[ "$python_env" == *"/envs/myenv"* ]]; then
    echo "[INFO] 가상환경 활성화: 성공"
else
    echo "[INFO] 가상환경 활성화: 실패"
    exit 1 
fi

# 필요한 패키지 설치
## TODO
pip install mypy

# Submission 폴더 파일 실행
cd submission || { echo "[INFO] submission 디렉토리로 이동 실패"; exit 1; }

for file in *.py; do
    # 경로에서 문제번호 추출
    filename=$(basename "$file" .py)      # "5_2243"
    problem_number=${filename#*_}

    # 파일 읽어 실행 후, 결과를 output 폴더에 .output 붙혀 저장
    python3 "$file" < "../input/${problem_number}_input" > "../output/${problem_number}_output"
done

cd ..

# mypy 테스트 실행 및 mypy_log.txt 저장
## TODO
mypy submission/ > mypy_log.txt 2>&1

# conda.yml 파일 생성
## TODO
conda env export > conda.yml

# 가상환경 비활성화
## TODO
conda deactivate