use proconio::input;

fn main() {
    input! {
        mut s: String,
    }
    let mut a = 0;
    let mut b = 0;
    let mut c = 0;
    for x in s.chars() {
        if x == 'a' {
            a += 1;
        } else if x == 'b' {
            b += 1;
        } else {
            c += 1;
        }
    }
    if a > b && a > c {
        println!("a");
    } else if b > a && b > c {
        println!("b");
    } else {
        println!("c");
    }
}
