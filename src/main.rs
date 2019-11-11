
extern crate rand;

use rand::distributions::WeightedIndex;
use rand::distributions::Distribution;

#[derive(PartialEq)]
#[derive(Debug)]
#[derive(Copy)]
#[derive(Clone)]
enum Choice {
    Rock,
    Paper,
    Scissors
}

fn compute_regret(p1_choice: &Choice, p2_choice: &Choice) -> Vec<f32> {
    match *p1_choice {
        Choice::Rock => match p2_choice {
            Choice::Rock     => return vec!(0., 1., 0.),
            Choice::Paper    => return vec!(0., 1., 2.),
            Choice::Scissors => return vec!(0., 0., 0.),
        },
        Choice::Paper => match p2_choice {
            Choice::Rock     => return vec!(0., 0., 0.),
            Choice::Paper    => return vec!(1., 0., 0.),
            Choice::Scissors => return vec!(2., 1., 0.),
        },
        Choice::Scissors => match p2_choice {
            Choice::Rock     => return vec!(1., 2., 0.),
            Choice::Paper    => return vec!(0., 0., 0.),
            Choice::Scissors => return vec!(1., 0., 0.),
        }
    }
}

fn compute_regret_matching_strategy_profile(
        hist: &[(Choice, Choice)]
    ) -> Vec<f32> {
    let mut cumulative_regret: Vec<f32> = vec!(0., 0., 0.);
    for pair in hist.iter() {
        let regret = compute_regret(&pair.0, &pair.1);
        for i in 0..cumulative_regret.len() {
            cumulative_regret[i] += regret[i];
        }
    }
    let total_regret =
        cumulative_regret.iter()
                         .fold(0., |acc,x| acc + x);
    return cumulative_regret.iter()
                            .map(|x| x/total_regret)
                            .collect()
}

fn get_choice(strategy: &Vec<f32>) -> Choice {
    let choices = [&Choice::Rock, &Choice::Paper, &Choice::Scissors];
    let dist = WeightedIndex::new(strategy).unwrap();
    let mut rng = rand::thread_rng();
    return *choices[dist.sample(&mut rng)]
}

fn main() {
    let mut hist: Vec<(Choice, Choice)> = Vec::new();
    let p1_strategy = vec![0.4, 0.2, 0.4];
    let p2_strategy = vec![0.33, 0.23, 0.44];
    for _ in 0..50 {
        let p1_choice = get_choice(&p1_strategy);
        let p2_choice = get_choice(&p2_strategy);
        let pair = (p1_choice, p2_choice);
        hist.push(pair);
    }
    let profile = compute_regret_matching_strategy_profile(&hist);
    println!("{:?}", profile);
}

