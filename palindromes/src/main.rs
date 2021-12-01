use std::error::Error;
use std::fs;
use std::str;

fn expand_center(s: &Vec<u8>, mut l: usize, mut r: usize) -> usize {
    while l > 0 && r < s.len() && s[l] == s[r] {
        l -= 1;
        r += 1;
    }
    return r - l;
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut s = fs::read("./palindrome.txt")?;
    //s.retain(|&x| x != 10_u8);
    println!("{:?}", str::from_utf8(&s[0..23]));

    let mut start = 0;
    let mut end = 0;
    for i in 0..s.len() {
        //center can be on a character (len1) or between(len2)
        let len1 = expand_center(&s, i, i);
        let len2 = expand_center(&s, i, i + 1);
        let len = len1.max(len2);

        if len > end - start {
            start = i - (len - 1) / 2;
            end = i + len / 2;
        }
    }
    println!("{}", str::from_utf8(&s[start..end])?);
    Ok(())
}
