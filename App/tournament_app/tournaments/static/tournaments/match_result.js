console.log('Js works')

const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value


document.querySelectorAll('.p1_result').forEach(button => {
    button.addEventListener('click', e => {
        e.preventDefault()
        const result = button.dataset.value
        const form = button.closest('form')
        const url = form.action

        const formData = new FormData()
        formData.append('result', result)

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
            
                console.log('Match updated successfully.', data)
                const p2DisplayID = `m${data.round_num}_${data.player_1}_vs_${data.player_2}_result`
                const p2Display = document.getElementById(p2DisplayID)
                const player_1 = document.getElementById(`m${data.round_num}_${data.player_1}`).innerText
                const player_2 = document.getElementById(`m${data.round_num}_${data.player_2}`).innerText 
                p2Display.textContent = `Result: ${player_1}: ${data.result} -- ${player_2}: ${data.p2_result}`
                console.log(`${player_1}: ${data.result} -- ${player_2}: ${data.p2_result}`)
                
            
            } else {
                console.error('Failed to update match.', data)
            }
        })
        .catch(error => {
            console.error('AJAX Error', error)
        })
    })
})
    
