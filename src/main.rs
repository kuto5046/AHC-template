#![allow(non_snake_case, unused_macros)]

// 定数
const TIME_LIMIT: f64 = 1.97;

fn main() {
    get_time();
    let cfg = Config {
        policy: Policy::Template
    };
    let solver = Solver::new(input, cfg)
    solver.solve();    
}

// パラメータ
struct Config {
    // パラメータを管理する構造体
    policy: Policy,
}
enum Policy {
    // 方策を列挙する
    Template
}


struct Solver {
    input: Input,
    cfg: Config,
}

impl Solver {
    fn new(input: Input, cfg: Config) -> Solver {
        Solver { input: input.clone(), cfg }
    }

    fn template(&mut self) -> Vec<usize> {
        let mut out = vec![];
        out
    }

    fn solve(&mut self){
        println!("Hello, world!");
        // let out = match self.cfg.policy {
        //     Policy::Template => self.template(),
        // };
    }

pub fn get_time() -> f64 {
    static mut STIME: f64 = -1.0;
    let t = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap();
    let ms = t.as_secs() as f64 + t.subsec_nanos() as f64 * 1e-9;
    unsafe {
        if STIME < 0.0 {
            STIME = ms;
        }
        // ローカル環境とジャッジ環境の実行速度差はget_timeで吸収しておくと便利
        #[cfg(feature = "local")]
        {
            (ms - STIME) * 1.0
        }
        #[cfg(not(feature = "local"))]
        {
            ms - STIME
        }
    }
}
