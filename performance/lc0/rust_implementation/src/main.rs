use std::process::{Command, Stdio};
use std::io::{self, Write, Read};
use std::thread;
use std::time::Duration;

fn main() -> io::Result<()> {
    // Substitua pelo caminho real para o executável lc0
    let lc0_path = "/home/nitro/wrkdir/ai.challenger/engines/lc0/lc0/build/release/lc0";
    // Substitua pelo caminho real para os pesos do LCZero
    let lc0_weights = "/home/nitro/wrkdir/ai.challenger/performance/lc0/rust_implementation/weights/768x15x24h-t82-2-swa-5230000.pb";

    // Comando para iniciar o LCZero com os pesos específicos
    let mut lc0_command = Command::new(lc0_path)
        .arg("-w")
        .arg(lc0_weights)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()?;

    let mut lc0_stdin = lc0_command.stdin.take().unwrap();
    let mut lc0_stdout = lc0_command.stdout.take().unwrap();

    // Exemplo de comando para enviar um movimento ao LCZero
    lc0_stdin.write_all(b"position startpos moves e2e4\n")?;
    lc0_stdin.write_all(b"go\n")?;

    // Ler a saída do LCZero
    let mut output = String::new();
    lc0_stdout.read_to_string(&mut output)?;

    println!("{}", output);

    // Enviar comando "isready" para iniciar a análise
    lc0_stdin.write_all(b"isready\n")?;
    thread::sleep(Duration::from_secs(1)); // Aguardar um segundo para dar tempo ao LCZero responder
    lc0_stdout.read_to_string(&mut output)?;

    println!("{}", output);

    // Finalizar o processo corretamente enviando "quit"
    lc0_stdin.write_all(b"quit\n")?;
    lc0_command.wait()?;  // Aguardar o processo terminar

    Ok(())
}
