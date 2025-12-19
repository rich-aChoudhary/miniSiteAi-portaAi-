
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

            if (response.ok) {
                const data = await response.json();
                previewDiv.innerHTML = data;
                editableDiv.innerHTML = data;
                editBtn.style.display = 'inline-block';
            } else {
                previewDiv.innerHTML = '❌ Failed to generate portfolio.';
                editBtn.style.display = 'none';
            }
        } catch (err) {
            console.error(err);
            previewDiv.innerHTML = '❌ Something went wrong.';
            editBtn.style.display = 'none';
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

// document.addEventListener('DOMContentLoaded', async () => {
//       const user = JSON.parse(localStorage.getItem('user') || '{}');
//       const container = document.getElementById('portfolio-table-body');
//       const preview = document.getElementById('portfolio-preview');
//       const editorSection = document.getElementById('portfolio-editor-section');
//       const editableDiv = document.getElementById('portfolio-editable');
//       const editBtn = document.getElementById('editPortfolioBtn');
//       const saveBtn = document.getElementById('savePortfolio');
//       const cancelBtn = document.getElementById('cancelEdit');
//       const imageUpload = document.getElementById('imageUpload');
//       const aiOutputSection = document.getElementById('ai-output');

//       if (!user.id) {
//         container.innerHTML = `<tr><td colspan="3" class="p-4 text-center text-red-500">❌ User not found. Please log in again.</td></tr>`;
//         return;
//       }

//       // Toggle between preview and edit modes
//       function toggleEditor(showEditor, htmlContent = '') {
//         if (showEditor) {
//           preview.style.display = 'none';
//           editorSection.style.display = 'block';
//           editBtn.style.display = 'none';
//           editableDiv.innerHTML = DOMPurify.sanitize(htmlContent);
//           aiOutputSection.style.display = 'block';
//         } else {
//           preview.style.display = 'block';
//           editorSection.style.display = 'none';
//           editBtn.style.display = 'block';
//           preview.innerHTML = DOMPurify.sanitize(editableDiv.innerHTML);
//           aiOutputSection.style.display = editableDiv.innerHTML.trim() ? 'block' : 'none';
//         }
//       }

//       // Show editor with content
//       function showEditorWithContent(html) {
//         toggleEditor(true, html);
//       }

//       // Image upload handler
//       imageUpload.addEventListener('change', (e) => {
//         const file = e.target.files[0];
//         if (file) {
//           const reader = new FileReader();
//           reader.onload = (event) => {
//             const img = document.createElement('img');
//             img.src = event.target.result;
//             img.className = 'max-w-full my-2';
//             editableDiv.appendChild(img);
//           };
//           reader.readAsDataURL(file);
//         }
//       });

//       // Save portfolio handler
//       saveBtn.addEventListener('click', async () => {
//         const portfolioId = editableDiv.dataset.currentId;
//         const content = DOMPurify.sanitize(editableDiv.innerHTML);
//         try {
//           const res = await fetch(`/api/save-portfolio/${portfolioId}`, {
//             method: 'PUT',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ content }),
//           });
//           if (res.ok) {
//             toggleEditor(false, content);
//             alert('Portfolio saved successfully!');
//           } else {
//             throw new Error('Failed to save portfolio');
//           }
//         } catch (err) {
//           console.error(err);
//           alert('❌ Failed to save portfolio.');
//         }
//       });

//       // Cancel edit handler
//       cancelBtn.addEventListener('click', () => {
//         toggleEditor(false);
//       });

//       // Edit portfolio button handler
//       editBtn.addEventListener('click', () => {
//         toggleEditor(true, editableDiv.innerHTML);
//       });

//       try {
//         const res = await fetch(`/api/my-portfolios/${user.id}`);
//         const portfolios = await res.json();

//         if (portfolios.length === 0) {
//           container.innerHTML = `<tr><td colspan="3" class="p-4 text-center text-gray-500">You have no portfolios yet.</td></tr>`;
//           return;
//         }

//         // Populate table body
//         container.innerHTML = portfolios.map(p => `
//           <tr class="hover:bg-gray-50">
//             <td class="p-4 border-b border-gray-200">${p.title}</td>
//             <td class="p-4 border-b border-gray-200">${p.created_at}</td>
//             <td class p-4 border-b border-gray-200">
//               <a href="/portfolio/${p.id}" target="_blank" class="inline-block bg-indigo-600 text-white px-3 py-1 rounded hover:bg-indigo-700">👁️ View</a>
//               <button data-id="${p.id}" class="edit-btn inline-block bg-emerald-600 text-white px-3 py-1 rounded hover:bg-emerald-700 ml-2">✏️ Edit</button>
//             </td>
//           </tr>
//         `).join('');

//         // Attach Edit event handlers
//         document.querySelectorAll('.edit-btn').forEach(btn => {
//           btn.addEventListener('click', async function () {
//             const portfolioId = this.dataset.id;
//             try {
//               const res = await fetch(`/api/portfolio/${portfolioId}`);
//               const  content = await res.json();
//               showEditorWithContent(content);
//               editableDiv.dataset.currentId = portfolioId;
//             } catch (err) {
//               console.error(err);
//               container.innerHTML = `<tr><td colspan="3" class="p-4 text-center text-red-500">❌ Failed to load portfolio content.</td></tr>`;
//             }
//           });
//         });

//       } catch (err) {
//         console.error(err);
//         container.innerHTML = `<tr><td colspan="3" class="p-4 text-center text-red-500">❌ Failed to load portfolios.</td></tr>`;
//       }
// });
