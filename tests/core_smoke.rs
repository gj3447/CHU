use std::process::Command;

#[test]
fn native_core_executes_all_semantic_assertions() {
    let result = Command::new(env!("CARGO_BIN_EXE_chu-core"))
        .output()
        .expect("run core");
    assert!(result.status.success(), "{}", String::from_utf8_lossy(&result.stderr));
    let stdout = String::from_utf8(result.stdout).unwrap();
    assert!(stdout.contains("ALL ASSERTS PASS"));
    assert!(stdout.contains("ALL UNIVALENT ASSERTS PASS"));
}
