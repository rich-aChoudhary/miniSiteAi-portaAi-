
document.addEventListener('DOMContentLoaded', function() {
    // 1. Social login/signup button handlers (not real yet, just shows a message)
    document.querySelectorAll('.social-btn').forEach(button => {
        button.addEventListener('click', function() {
            const provider = this.textContent;
            alert(`Login/Signup with ${provider} is not ready yet.`);
        });
    });

    // 2. Get Started button: Go to dashboard if logged in, else go to register page
    const getStartedButton = document.getElementById('getStarted');
    if (getStartedButton) {
        getStartedButton.addEventListener('click', function() {
            if (localStorage.getItem('user')) {
                window.location.href = '/dashboard';
            } else {
                window.location.href = '/register';
            }
        });
    }

    // 3. Login and Signup buttons
    const loginButton = document.getElementById('loginButton');
    if (loginButton) {
        loginButton.addEventListener('click', function() {
            window.location.href = '/login';
        });
    }
    const signupButton = document.getElementById('signupButton');
    if (signupButton) {
        signupButton.addEventListener('click', function() {
            window.location.href = '/register';
        });
    }

    // 4. Show or hide password when you click the eye icon
    const passwordToggle = document.querySelector('.password-toggle');
    if (passwordToggle) {
        passwordToggle.addEventListener('click', function() {
            togglePassword(); // This function should show/hide password
        });
    }


    // 7. Portfolio related elements
    const generatePortfolio = document.getElementById('generatePortfolio'); // Button to make portfolio
    const editBtn = document.getElementById('editPortfolioBtn'); // Edit button
    const previewDiv = document.getElementById('portfolio-preview'); // Where you see your portfolio
    const editableDiv = document.getElementById('portfolio-editable'); // Where you can edit
    const editorSection = document.getElementById('portfolio-editor-section'); // Editor area

    // 8. When you click 'Generate Portfolio', ask AI to make it for you!
   if (generatePortfolio) {
    generatePortfolio.addEventListener('click', async function () {

        const title = document.getElementById('title').value.trim();
        const descriptionInput = document.getElementById('description').value.trim();
        const fileInput = document.getElementById('resumeUpload').files[0];

        const outputSection = document.getElementById('ai-output');

        if (!title) {
            alert('Please enter portfolio title.');
            return;
        }

        if (!descriptionInput && !fileInput) {
            alert('Please add a description or upload a resume.');
            return;
        }

        previewDiv.innerHTML = '⏳ Generating your portfolio...';
        outputSection.style.display = 'block';
        editorSection.style.display = 'none';
        editableDiv.innerHTML = '';

        // Ensure loader element exists and show it
        let loader = document.getElementById('ai-loader');
        if (!loader) {
            loader = document.createElement('div');
            loader.id = 'ai-loader';
            loader.className = 'loader-overlay';
            const spinner = document.createElement('div');
            spinner.className = 'spinner';
            loader.appendChild(spinner);
            document.body.appendChild(loader);
        }
        loader.style.display = 'flex';

        let finalDescription = descriptionInput;

        // 📄 Extract text from file if uploaded
        if (fileInput) {
            try {
                const extractedText = await extractTextFromFile(fileInput);

                if (!finalDescription) {
                    finalDescription = extractedText;
                } else {
                    finalDescription += '\n\n' + extractedText;
                }
            } catch (err) {
                alert('Failed to read resume file.');
                return;
            }
        }

        const user = JSON.parse(localStorage.getItem('user') || '{}');

        try {
            const response = await fetch('/api/generate-portfolio', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    userId: user.id,
                    title: title,
                    data: finalDescription
                })
            });

            // Always hide loader when we have a response
            const data = await response.json();
            loader.style.display = 'none';
            if (response.ok) {
                if (data.portfolio_id) {
                    window.location.href = `/portfolio/${data.portfolio_id}`;
                } else {
                    alert('Failed to Portfolio ');
                }
            } else {
               alert(data.message || 'Failed to generate portfolio.');
            }
        } catch (err) {
            console.error(err);
          alert('Error generating portfolio. Please try again.');
        }
    });
}


    async function extractTextFromFile(file) {
    const ext = file.name.split('.').pop().toLowerCase();

    // PDF
    if (ext === 'pdf') {
        const arrayBuffer = await file.arrayBuffer();
        const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;

        let text = '';
        for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const content = await page.getTextContent();
            text += content.items.map(item => item.str).join(' ') + '\n';
        }
        return text.trim();
    }

    // DOC / DOCX (basic fallback)
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsText(file);
    });
}

    // 9. When you click 'Edit', show the editor with your portfolio content
    if (editBtn) {
        editBtn.addEventListener('click', () => {
            showEditorWithContent(previewDiv.innerHTML);
        });
    }


});
