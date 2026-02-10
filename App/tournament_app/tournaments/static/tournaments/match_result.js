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
                const p2Display = form.querySelector('.p2_result')

                p2Display.classList.remove('no_dihsplay')
                p2Display.textContent = `${data.p2_result}`
            } else {
                console.error('Failed to update match.', data)
            }
        })
        .catch(error => {
            console.error('AJAX Error', error)
        })
    })
})
    
