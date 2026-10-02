async function generate(){
    const age = document.getElementById('age').value;
    const weight = document.getElementById('weight').value;
    const goal = document.getElementById('goal').value;
    if(!age || !weight){ alert('Age and Weight fill pannu'); return; }

    document.getElementById('plan').innerHTML = "Generating... ⏳";

    const res = await fetch('/generate-plan', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({age, weight, goal})
    });
    const data = await res.json();
    document.getElementById('plan').innerText = data.plan;
}
