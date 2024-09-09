import subprocess
from datetime import datetime
import time
import logging

# import pandas as pd
from pathlib import Path
from collections import defaultdict
import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from typing import DefaultDict

class CFG:
    version = "exp001"
    output_dir = Path(f"./output/{version}")
    n_test = 100
    comment = "sample"


def get_timestamp() -> str:
    # output config
    return datetime.today().strftime("%m%d_%H%M%S")


def get_logger(output_dir: Path, file_name: str = "result.log") -> logging.Logger:
    """
    from src.utils import get_logger
    logger = get_logger(output_dir)
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # File handler for outputting to a log file
    file_handler = logging.FileHandler(output_dir / file_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def main():
    timestamp = get_timestamp()
    CFG.output_dir.mkdir(exist_ok=True, parents=True)
    Path("./output/latest").mkdir(exist_ok=True, parents=True)
    logger = get_logger(CFG.output_dir, f"{timestamp}.log")
    for k, v in CFG.__dict__.items():
        if k in ["version", "n_test", "comment"]:
            logger.info(f"{k}: {v}")

    logger.info("#" * 30)
    logger.info("evaluate start")
    start_ts = time.time()
    test_files = [str(i).zfill(4) for i in range(CFG.n_test)]
    results: DefaultDict[str, list[float | int]] = defaultdict(list)
    for test_file in tqdm(test_files):
        # 標準出力を./output/{test_file}.txtに保存する
        cmd = f"cargo run --release --bin=main --features 'local' < ./input/{test_file}.txt > ./output/latest/{test_file}.txt"
        # 標準出力を取得する
        process = (
            subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            ).communicate()[1]
        ).decode("utf-8")
        # process = (subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                         shell=True).communicate()[0]).decode('utf-8')

        score = int(process.split("\n")[-3].split(":")[-1].strip())
        # ./input/{test_file}.txtの先頭の1行を読み込む
        # with open(f"./input/{test_file}.txt", "r") as f:
        #     first_line = f.readline().strip()
        # w, d, n = map(float, first_line.split())
        if score > 0:
            results["score"].append(score)
            # TODO: スコアと合わせてみたいパラメータがあれば追加する
            # results["param1"].append(param)
        logger.info(f"test:{test_file} {score}")

    # pd.DataFrame(results).to_csv(CFG.output_dir / f'result.csv', index=False)
    spend_time = time.time() - start_ts
    logger.info("#" * 30)
    logger.info(f'avg final score: {np.mean(results["score"])}')
    logger.info(f'total score: {np.sum(results["score"])}')
    logger.info(f"spend time: {int(spend_time)}s")

    print(f'avg final score: {np.mean(results["score"])}')

    df = pd.DataFrame(results)
    df.to_csv(CFG.output_dir / f"{timestamp}.csv", index=False)

    # main.rsファイルをexp_name.rsに変換してsnapshotディレクトリに保存
    snapshot_dir = CFG.output_dir / "snapshot"
    snapshot_dir.mkdir(exist_ok=True, parents=True)
    subprocess.run(
        f"cp ./src/main.rs {snapshot_dir}/{CFG.version}_{timestamp}.rs", shell=True
    )


if __name__=="__main__":
    main()