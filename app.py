from shiny import App, ui, render, reactive
import htmltools as tags
from datetime import datetime
import os
import requests
from urllib.parse import urlparse
import base64
from openpyxl import Workbook
import io
from PIL import Image, ImageDraw, ImageFont
import textwrap

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

waiver_content = {
    "en": {
        "title": "BICYCLE PROGRAM WAIVER AND RELEASE FROM LIABILITY",
        "logo_text1": "HOPE'S CORNER",
        "logo_subtext": "SHARING MEALS, BUILDING COMMUNITY",
        "intro": "I expressly assume and accept any and all risk of injury or death to myself or others arising from my use of the Hope's Corner, Inc. Bicycle Program including repair services, transportation equipment such as bicycles, scooters, skateboards, etc. and all equipment and supplies. This waiver and release from liability includes any and all repair services, equipment, including but not limited to, the bicycle, helmet, lock, light, rack, basket, tubes, tires, chains, brakes, and my participation in the Program.",
        "points": [
            "I am a voluntary participant and utilize the program services and equipment at my own risk.",
            "I am responsible for maintaining the bicycle in good condition. I will inspect the bicycle prior to use to ensure all parts are in proper working condition.",
            "I understand that there are risks inherent in riding a bicycle even when the bicycle and equipment are in good working order and used properly. Injuries are a common, ordinary and foreseeable consequence of bicycle riding. I understand that the risks I may encounter include, but are not limited to the following:",
        ],
        "sub_points": [
            "The equipment may break or malfunction, causing loss of or damage to property or injury to my person or to another person.",
            "Riding a bicycle requires physical exertion and may result in discomfort, pain or injury.",
            "I might encounter hazards while riding which could cause me to fall or be propelled.",
            "Bicycle travel is dangerous. I may be injured by many factors over which I have no control.",
        ],
        "volunteer_clause": "I understand that I assume the risk of any damage or failure of equipment arising from repair work or services donated to me by the Bicycle Program volunteers, employees or vendors. I understand the program volunteers and employees are not trained or licensed professionals and cannot be held responsible for damage to my equipment. I am responsible for inspecting the work and not utilizing the bicycle or equipment if it is not in good working order.",
        "indemnify_clause": "I agree to indemnify, defend, save and hold harmless Hope's Corner, Inc. including all employees, volunteers, directors, officers, vendors and funders of the program from any claims, losses, damages or liability accruing or resulting to any person or entity from my participation in the Bicycle Program or use of the bicycle, bicycle equipment and bicycle repair services.",
        "release_clause": "I, on behalf of myself, my heirs, successors and assigns, hereby waive, release and forever discharge Hope's Corner, Inc. including all employees, volunteers, directors, officers, vendors and funders of the program from any and all claims, losses, damages or liability accruing or resulting to any person or entity from my participation in the Bicycle Program or use of the bicycle, bicycle equipment and repair services.",
        "final_agreement": "I AM AWARE THAT THIS IS A RELEASE OF LIABILITY. I AM SIGNING IT FREELY AND OF MY OWN ACCORD AND I RECOGNIZE AND AGREE THAT IT IS BINDING UPON MYSELF, MY HEIRS AND ASSIGNS, AND IN THE EVENT THAT I AM SIGNING IT ON BEHALF OF ANY MINORS, I HAVE FULL LEGAL AUTHORITY TO DO SO, AND REALIZE THE BINDING EFFECT OF THIS CONTRACT ON THEM, AS WELL AS ON MYSELF. I AGREE TO ALLOW HOPE'S CORNER, INC. TO USE PHOTOGRAPHS, VIDEOS, OR SOUND RECORDINGS OF ME FOR PROMOTIONAL AND PUBLICITY PURPOSES.",
        "agreement_check": "I have carefully read this agreement and understand that this is a release of liability. I agree to the terms and conditions.",
        "print_name_label": "Print Full Name",
        "signature_label": "Signature (Draw below)",
        "date_label": "Date",
        "submit_button": "Submit Waiver",
        "switch_button": "Leer en Español",
        "success_message": "Thank you! Your waiver has been submitted successfully.",
        "signature_placeholder": "Type your signature here or upload an image",
    },
    "es": {
        "title": "PROGRAMA DE BICICLETAS ACUERDO DE RENUNCIA Y EXENCIÓN DE RESPONSABILIDAD",
        "logo_text1": "HOPE'S CORNER",
        "logo_subtext": "COMPARTIR COMIDAS, CONSTRUYENDO COMUNIDAD",
        "intro": "Asumo y acepto expresamente todos y cada uno de los riesgos de lesiones o muerte para mí u otros que surjan de mi uso del Programa de Bicicletas de Hope's Corner, Inc., incluidos los servicios de reparación, equipos de transporte como bicicletas, scooters, patinetas, etc., y todo el equipo y los suministros. Esta renuncia y exención de responsabilidad incluye todos y cada uno de los servicios de reparación, equipos, incluidos, entre otros, la bicicleta, el casco, el candado, la luz, el portabultos, la canasta, las cámaras, los neumáticos, las cadenas, los frenos y mi participación en el Programa.",
        "points": [
            "Soy un participante voluntario y utilizo los servicios y el equipo del programa bajo mi propio riesgo.",
            "Soy responsable de mantener la bicicleta en buenas condiciones. Inspeccionaré la bicicleta antes de usarla para asegurarme de que todas las piezas estén en condiciones de funcionamiento adecuadas.",
            "Entiendo que existen riesgos inherentes al andar en bicicleta incluso cuando la bicicleta y el equipo están en buen estado de funcionamiento y se utilizan correctamente. Las lesiones son una consecuencia común, ordinaria y previsible de andar en bicicleta. Entiendo que los riesgos que puedo encontrar incluyen, entre otros, los siguientes:",
        ],
        "sub_points": [
            "El equipo puede romperse o funcionar mal, causando pérdidas o daños a la propiedad o lesiones a mi persona o a otra persona.",
            "Andar en bicicleta requiere esfuerzo físico y puede provocar molestias, dolor o lesiones.",
            "Podría encontrar peligros mientras conduzco que podrían hacer que me caiga o sea impulsado.",
            "Viajar en bicicleta es peligroso. Puedo resultar herido por muchos factores sobre los que no tengo control.",
        ],
        "volunteer_clause": "Entiendo que asumo el riesgo de cualquier daño o falla del equipo que surja del trabajo de reparación o los servicios que me donen los voluntarios, empleados o proveedores del Programa de Bicicletas. Entiendo que los voluntarios y empleados del programa no son profesionales capacitados o con licencia y no se les puede hacer responsables de los daños a mi equipo. Soy responsible de inspeccionar el trabajo y no utilizar la bicicleta o el equipo si no está en buen estado de funcionamiento.",
        "indemnify_clause": "Acepto indemnizar, defender, salvar y mantener indemne a Hope's Corner, Inc., incluidos todos los empleados, voluntarios, directores, funcionarios, proveedores y financiadores del programa de cualquier reclamo, pérdida, daño o responsabilidad que se acumule o resulte para cualquier persona o entidad de mi participación en el Programa de Bicicletas o el uso de la bicicleta, el equipo de la bicicleta y los servicios de reparación de bicicletas.",
        "release_clause": "Yo, en mi nombre, mis herederos, sucesores y cesionarios, por la presente renuncio, libero y descargo para siempre a Hope's Corner, Inc., incluidos todos los empleados, voluntarios, directores, funcionarios, proveedores y financiadores del programa de cualquier y todos los reclamos, pérdidas, daños o responsabilidad que se acumulen o resulten para cualquier persona o entidad de mi participación en el Programa de Bicicletas o el uso de la bicicleta, el equipo de la bicicleta y los servicios de reparación.",
        "final_agreement": "SOY CONSCIENTE DE QUE ESTA ES UNA EXENCIÓN DE RESPONSABILIDAD. LO FIRMO LIBREMENTE Y POR MI PROPIA VOLUNTAD Y RECONOZCO Y ACEPTO QUE ES VINCULANTE PARA MÍ, MIS HEREDEROS Y CESIONARIOS, Y EN CASO DE QUE LO FIRME EN NOMBRE DE MENORES, TENGO PLENA AUTORIDAD LEGAL PARA HACERLO, Y ME DOY CUENTA DEL EFECTO VINCULANTE DE ESTE CONTRATO SOBRE ELLOS, ASÍ COMO SOBRE MÍ. ACEPTO PERMITIR QUE HOPE'S CORNER, INC. UTILICE FOTOGRAFÍAS, VIDEOS O GRABACIONES DE SONIDO DE MÍ PARA FINES PROMOCIONALES Y PUBLICITARIOS.",
        "agreement_check": "He leído atentamente este acuerdo y entiendo que se trata de una exención de responsabilidad. Acepto los términos y condiciones.",
        "print_name_label": "Escriba el Nombre Completo",
        "signature_label": "Firma (Dibuje abajo)",
        "date_label": "Fecha",
        "submit_button": "Enviar Renuncia",
        "switch_button": "Read in English",
        "success_message": "¡Gracias! Su renuncia ha sido enviada con éxito.",
        "signature_placeholder": "Escriba su firma aquí o suba una imagen",
    },
}


def create_header(content, language):
    return tags.div(
        tags.div(
            tags.div(
                ui.input_action_button(
                    "language_switch",
                    content["switch_button"],
                    class_="btn btn-outline-success btn-sm",
                ),
                style="position: absolute; top: 1rem; right: 1rem; z-index: 10;",
            ),
            tags.div(
                tags.img(
                    src="https://images.squarespace-cdn.com/content/v1/5622cd82e4b0501d40689558/cdab4aef-0027-40b7-9737-e2f893586a6a/Hopes_Corner_Logo_Green.png?format=500w",
                    alt="Hope's Corner Logo",
                    style="height: 80px; object-fit: contain; background: rgba(255,255,255,0.95); padding: 8px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;",
                ),
                tags.h1(content["logo_text1"], class_="h3 fw-bold text-white mb-1"),
                tags.p(content["logo_subtext"], class_="small text-white-50 mb-0"),
                class_="text-center",
            ),
            class_="bg-dark text-dark p-4 position-relative",
            style="background: linear-gradient(135deg, #166534 0%, #15803d 100%) !important;",
        )
    )


def create_waiver_content(content):
    return ui.tags.div(
        ui.tags.h3(content["title"], class_="h4 fw-bold text-center mb-4"),
        ui.tags.div(
            ui.tags.p(content["intro"], class_="mb-3"),
            ui.tags.ol(
                ui.tags.li(content["points"][0], class_="mb-2"),
                ui.tags.li(content["points"][1], class_="mb-2"),
                ui.tags.li(
                    content["points"][2],
                    ui.tags.ol(
                        *[
                            ui.tags.li(point, class_="mb-1")
                            for point in content["sub_points"]
                        ],
                        type="a",
                        class_="mt-2 ps-3",
                    ),
                    class_="mb-2",
                ),
                class_="ps-3",
            ),
            tags.p(content["volunteer_clause"], class_="mb-3"),
            tags.p(content["indemnify_clause"], class_="mb-3"),
            tags.p(content["release_clause"], class_="mb-3"),
            tags.div(
                tags.p(
                    content["final_agreement"], class_="fw-bold small text-uppercase"
                ),
                class_="alert alert-warning border-start border-warning border-4 bg-warning bg-opacity-10",
            ),
            class_="small lh-base",
        ),
    )


def create_form_section(content):
    return tags.div(
        ui.tags.hr(class_="my-4"),
        ui.tags.div(
            ui.input_checkbox("agreement", content["agreement_check"], value=False),
            class_="mb-4",
        ),
        ui.tags.div(
            ui.tags.div(
                ui.input_text(
                    "participant_name",
                    content["print_name_label"],
                    placeholder="Enter your full name",
                ),
                class_="col-md-6 mb-3",
            ),
            ui.tags.div(
                ui.tags.label(
                    content["signature_label"], class_="form-label fw-medium"
                ),
                ui.tags.div(
                    ui.tags.canvas(
                        id="signature-canvas",
                        width="400",
                        height="150",
                        style="border: 2px solid #ddd; border-radius: 8px; cursor: crosshair; touch-action: none; width: 100%; max-width: 400px; background: white;",
                    ),
                    ui.tags.div(
                        ui.tags.button(
                            "Clear Signature",
                            type="button",
                            id="clear-signature",
                            class_="btn btn-outline-secondary btn-sm me-2",
                        ),
                        ui.tags.span(
                            "✓",
                            id="signature-check",
                            style="color: green; font-weight: bold; display: none;",
                        ),
                        class_="mt-2",
                    ),
                    ui.tags.div(
                        "Sign here with your finger or mouse",
                        class_="text-muted small mt-1",
                    ),
                ),
                ui.tags.div(
                    ui.input_text(
                        "signature_data",
                        None,
                        value="",
                    ),
                    style="display: none;",
                ),
                class_="col-md-6 mb-3",
            ),
            class_="row",
        ),
        ui.tags.div(
            ui.output_text("current_date_display"),
            class_="mb-4 p-3 bg-light rounded",
        ),
        ui.tags.div(
            ui.input_action_button(
                "submit_waiver",
                content["submit_button"],
                class_="btn btn-primary btn-lg",
                disabled=True,
            ),
            class_="text-end",
        ),
    )


app_ui = ui.page_fluid(
    ui.tags.style(
        """
        body { 
            background-color: #f8f9fa; 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
        }
        .waiver-container { 
            max-width: 800px; 
            margin: 2rem auto; 
            background: white; 
            border-radius: 12px; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .form-control:focus, .form-check-input:focus {
            border-color: #0d6efd;
            box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
        }
        .success-message {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            border: 1px solid #c3e6cb;
            border-radius: 8px;
            padding: 3rem;
            text-align: center;
            margin: 2rem 0;
        }
        .checkmark {
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: #28a745;
            color: white;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        #signature-canvas {
            touch-action: none;
        }
        .waiver-container * {
            -webkit-print-color-adjust: exact !important;
            color-adjust: exact !important;
        }
        input[type="checkbox"]:checked {
            background-color: #0d6efd !important;
        }
        input[type="text"], input[type="email"] {
            border: 1px solid #ced4da !important;
            background-color: white !important;
        }
    #submitting-overlay { position: fixed; inset: 0; display: none; align-items: center; justify-content: center; z-index: 2000; background: rgba(0,0,0,0.45); }
    #submitting-overlay .inner { color: #fff; font-weight: 500; font-size: 1.1rem; display:flex; align-items:center; gap:.75rem; }
    """
    ),
    ui.tags.script(
        """
        document.addEventListener('DOMContentLoaded', function() {
            let canvas = null;
            let ctx = null;
            let isDrawing = false;
            let lastX = 0;
            let lastY = 0;
            
            function initCanvas() {
                canvas = document.getElementById('signature-canvas');
                if (!canvas) {
                    setTimeout(initCanvas, 100);
                    return;
                }
                
                ctx = canvas.getContext('2d');
                ctx.strokeStyle = '#000';
                ctx.lineWidth = 2;
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
                
                const rect = canvas.getBoundingClientRect();
                canvas.width = rect.width * window.devicePixelRatio;
                canvas.height = 150 * window.devicePixelRatio;
                ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
                
                canvas.addEventListener('mousedown', startDrawing);
                canvas.addEventListener('mousemove', draw);
                canvas.addEventListener('mouseup', stopDrawing);
                canvas.addEventListener('mouseout', stopDrawing);
                
                canvas.addEventListener('touchstart', handleTouch);
                canvas.addEventListener('touchmove', handleTouch);
                canvas.addEventListener('touchend', stopDrawing);
                
                const clearBtn = document.getElementById('clear-signature');
                if (clearBtn) {
                    clearBtn.addEventListener('click', clearCanvas);
                }
            }
            
            function getPos(e) {
                const rect = canvas.getBoundingClientRect();
                const clientX = e.clientX || (e.touches && e.touches[0].clientX);
                const clientY = e.clientY || (e.touches && e.touches[0].clientY);
                return {
                    x: clientX - rect.left,
                    y: clientY - rect.top
                };
            }
            
            function startDrawing(e) {
                isDrawing = true;
                const pos = getPos(e);
                lastX = pos.x;
                lastY = pos.y;
            }
            
            function draw(e) {
                if (!isDrawing) return;
                e.preventDefault();
                
                const pos = getPos(e);
                ctx.beginPath();
                ctx.moveTo(lastX, lastY);
                ctx.lineTo(pos.x, pos.y);
                ctx.stroke();
                
                lastX = pos.x;
                lastY = pos.y;
                
                updateSignatureData();
            }
            
            function stopDrawing() {
                isDrawing = false;
                updateSignatureData();
            }
            
            function handleTouch(e) {
                e.preventDefault();
                const touch = e.touches[0];
                const mouseEvent = new MouseEvent(e.type === 'touchstart' ? 'mousedown' : 
                                                  e.type === 'touchmove' ? 'mousemove' : 'mouseup', {
                    clientX: touch.clientX,
                    clientY: touch.clientY
                });
                canvas.dispatchEvent(mouseEvent);
            }
            
            function clearCanvas() {
                if (ctx) {
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    updateSignatureData();
                }
            }
            
            function updateSignatureData() {
                if (canvas) {
                    const dataURL = canvas.toDataURL();
                    const input = document.getElementById('signature_data');
                    if (input) {
                        input.value = dataURL;
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                        input.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                    
                        const isEmpty = isCanvasEmpty();
                    const checkmark = document.getElementById('signature-check');
                    if (checkmark) {
                        checkmark.style.display = isEmpty ? 'none' : 'inline';
                    }
                }
            }
            
            function isCanvasEmpty() {
                if (!canvas) return true;
                const blank = document.createElement('canvas');
                blank.width = canvas.width;
                blank.height = canvas.height;
                return canvas.toDataURL() === blank.toDataURL();
            }
            
            initCanvas();
        });
        
        async function captureScreenshot(){
            console.log('[JS] captureScreenshot called');
            if(!window.html2canvas) {
                console.error('[JS] html2canvas not available');
                return;
            }
            try{
                const target = document.querySelector('.waiver-container') || document.body;
                console.log('[JS] Target element for capture:', target);
                window.scrollTo(0,0);
                
                const canvas = await html2canvas(target, {
                    scale: 1,
                    backgroundColor: '#ffffff',
                    useCORS:true,
                    logging:true,
                    allowTaint: false,
                    height: target.scrollHeight,
                    width: target.scrollWidth,
                    ignoreElements: el => {
                        const ignore = el.id==='page_screenshot' || el.id==='signature_data' || el.id==='submitting-overlay';
                        if (ignore) console.log('[JS] Ignoring element:', el.id);
                        return ignore;
                    }
                });
                
                console.log('[JS] Canvas created:', canvas.width, 'x', canvas.height);
                const dataURL = canvas.toDataURL('image/png');
                console.log('[JS] DataURL created, length:', dataURL.length);
                
                const input = document.getElementById('page_screenshot');
                console.log('[JS] Input element found:', !!input);
                if (input){
                    console.log('[JS] Current input value length:', input.value.length);
                    if (!input.value || input.value.length < 100) {
                        input.value = dataURL;
                        console.log('[JS] Set input value, new length:', input.value.length);
                        input.dispatchEvent(new Event('input',{bubbles:true}));
                        input.dispatchEvent(new Event('change',{bubbles:true}));
                        if(window.Shiny && window.Shiny.setInputValue){
                            console.log('[JS] Using Shiny.setInputValue');
                            Shiny.setInputValue('page_screenshot', dataURL, {priority:'event'});
                        }
                    } else {
                        console.log('[JS] Input already has screenshot data');
                    }
                } else {
                    console.error('[JS] page_screenshot input not found');
                }
            }catch(err){ 
                console.error('[JS] captureScreenshot error', err); 
            }
        }

        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(function() {
                const submitButton = document.querySelector('button[id*="submit_waiver"]');
                if (submitButton) {
                    console.log('[JS] Found submit button, adding screenshot capture listener');
                    submitButton.addEventListener('click', function(event) {
                        console.log('[JS] Submit button clicked - capturing screenshot immediately');
                        const overlay = document.getElementById('submitting-overlay');
                        if (overlay) overlay.style.display = 'flex';
                        
                        setTimeout(() => {
                            console.log('[JS] Attempting immediate screenshot capture');
                            captureScreenshot().catch((err) => {
                                console.error('[JS] Immediate capture failed:', err);
                            });
                        }, 200);
                    }, true);
                } else {
                    console.log('[JS] Submit button not found');
                }
            }, 1000);
        });
        """
    ),
    ui.tags.script(
        """
        let screenshotMethods = {
            html2canvas: null,
            fallback: null
        };

        function loadHtml2Canvas() {
            return new Promise((resolve) => {
                if (window.html2canvas) {
                    screenshotMethods.html2canvas = window.html2canvas;
                    resolve(true);
                    return;
                }
                
                const script = document.createElement('script');
                script.src = 'https://html2canvas.hertzen.com/dist/html2canvas.min.js';
                script.onload = () => {
                    screenshotMethods.html2canvas = window.html2canvas;
                    console.log('[JS] html2canvas loaded successfully');
                    resolve(true);
                };
                script.onerror = () => {
                    console.log('[JS] html2canvas failed to load, will use fallback');
                    resolve(false);
                };
                document.head.appendChild(script);
            });
        }

        function captureWithCanvas() {
            return new Promise((resolve) => {
                try {
                    const waiver = document.querySelector('.waiver-container');
                    if (!waiver) {
                        resolve(null);
                        return;
                    }

                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    
                    canvas.width = waiver.scrollWidth;
                    canvas.height = waiver.scrollHeight;
                    
                    ctx.fillStyle = '#ffffff';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    
                    ctx.fillStyle = '#000000';
                    ctx.font = '14px Arial';
                    
                    const text = waiver.innerText || 'Waiver content captured';
                    const lines = text.split('\\n');
                    let y = 30;
                    
                    lines.forEach(line => {
                        if (y < canvas.height - 20) {
                            ctx.fillText(line.substring(0, 80), 20, y);
                            y += 20;
                        }
                    });
                    
                    const sigCanvas = document.getElementById('signature-canvas');
                    if (sigCanvas) {
                        try {
                            ctx.drawImage(sigCanvas, 20, y + 20);
                        } catch (e) {
                            console.log('[JS] Could not copy signature canvas');
                        }
                    }
                    
                    resolve(canvas.toDataURL('image/png'));
                } catch (error) {
                    console.error('[JS] Canvas fallback error:', error);
                    resolve(null);
                }
            });
        }

        function captureWithSVG() {
            return new Promise((resolve) => {
                try {
                    const waiver = document.querySelector('.waiver-container');
                    if (!waiver) {
                        resolve(null);
                        return;
                    }

                    const serializer = new XMLSerializer();
                    const rect = waiver.getBoundingClientRect();
                    
                    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                    svg.setAttribute('width', rect.width);
                    svg.setAttribute('height', rect.height);
                    
                    const foreignObject = document.createElementNS('http://www.w3.org/2000/svg', 'foreignObject');
                    foreignObject.setAttribute('width', '100%');
                    foreignObject.setAttribute('height', '100%');
                    
                    const clonedWaiver = waiver.cloneNode(true);
                    foreignObject.appendChild(clonedWaiver);
                    svg.appendChild(foreignObject);
                    
                    const svgString = serializer.serializeToString(svg);
                    const dataURL = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgString);
                    
                    resolve(dataURL);
                } catch (error) {
                    console.error('[JS] SVG capture error:', error);
                    resolve(null);
                }
            });
        }

        async function captureScreenshot() {
            console.log('[JS] Starting enhanced screenshot capture...');
            
            await new Promise(resolve => setTimeout(resolve, 500));
            
            const nameInput = document.querySelector('input[id*="participant_name"]');
            const agreementCheckbox = document.querySelector('input[id*="agreement"]');
            
            if (nameInput && nameInput.value) {
                console.log('[JS] Name input value:', nameInput.value);
                nameInput.style.border = '1px solid #ced4da';
                nameInput.style.backgroundColor = 'white';
                nameInput.style.color = 'black';
            }
            
            if (agreementCheckbox) {
                console.log('[JS] Agreement checkbox checked:', agreementCheckbox.checked);
                if (agreementCheckbox.checked) {
                    agreementCheckbox.style.backgroundColor = '#0d6efd';
                    agreementCheckbox.style.borderColor = '#0d6efd';
                }
            }
            
            let result = null;
            
            // Try html2canvas first
            if (screenshotMethods.html2canvas) {
                try {
                    console.log('[JS] Attempting html2canvas capture...');
                    const target = document.querySelector('.waiver-container') || document.body;
                    window.scrollTo(0, 0);
                    
                    const canvas = await screenshotMethods.html2canvas(target, {
                        scale: 1.5,
                        backgroundColor: '#ffffff',
                        useCORS: true,
                        allowTaint: false,
                        logging: false,
                        height: target.scrollHeight,
                        width: target.scrollWidth,
                        onclone: function(clonedDoc) {
                            const clonedNameInput = clonedDoc.querySelector('input[id*="participant_name"]');
                            const clonedCheckbox = clonedDoc.querySelector('input[id*="agreement"]');
                            
                            if (clonedNameInput && nameInput && nameInput.value) {
                                clonedNameInput.value = nameInput.value;
                                clonedNameInput.setAttribute('value', nameInput.value);
                                clonedNameInput.style.color = 'black';
                                clonedNameInput.style.backgroundColor = 'white';
                                clonedNameInput.style.border = '1px solid #ced4da';
                            }
                            
                            if (clonedCheckbox && agreementCheckbox) {
                                clonedCheckbox.checked = agreementCheckbox.checked;
                                if (agreementCheckbox.checked) {
                                    clonedCheckbox.setAttribute('checked', 'checked');
                                    clonedCheckbox.style.backgroundColor = '#0d6efd';
                                    clonedCheckbox.style.borderColor = '#0d6efd';
                                }
                            }
                            
                            const allInputs = target.querySelectorAll('input, textarea, select');
                            const clonedInputs = clonedDoc.querySelectorAll('input, textarea, select');
                            
                            allInputs.forEach((input, index) => {
                                if (clonedInputs[index]) {
                                    clonedInputs[index].value = input.value;
                                    if (input.type === 'checkbox' || input.type === 'radio') {
                                        clonedInputs[index].checked = input.checked;
                                    }
                                }
                            });
                        },
                        ignoreElements: (el) => {
                            return el.id === 'page_screenshot' || 
                                   el.id === 'signature_data' || 
                                   el.id === 'submitting-overlay';
                        }
                    });
                    
                    result = canvas.toDataURL('image/png');
                    console.log('[JS] html2canvas capture successful, size:', result.length);
                } catch (error) {
                    console.error('[JS] html2canvas capture failed:', error);
                }
            }
            
            if (!result) {
                console.log('[JS] Attempting enhanced canvas fallback...');
                result = await captureWithEnhancedCanvas();
                if (result) {
                    console.log('[JS] Enhanced canvas fallback successful, size:', result.length);
                }
            }
            
            if (!result) {
                console.log('[JS] Attempting SVG fallback...');
                result = await captureWithSVG();
                if (result) {
                    console.log('[JS] SVG fallback successful, size:', result.length);
                }
            }
            
            if (result) {
                const input = document.getElementById('page_screenshot');
                if (input) {
                    input.value = result;
                    input.dispatchEvent(new Event('input', {bubbles: true}));
                    input.dispatchEvent(new Event('change', {bubbles: true}));
                    
                    if (window.Shiny && window.Shiny.setInputValue) {
                        Shiny.setInputValue('page_screenshot', result, {priority: 'event'});
                    }
                    
                    console.log('[JS] Screenshot saved to input field');
                } else {
                    console.error('[JS] page_screenshot input not found');
                }
            } else {
                console.error('[JS] All screenshot methods failed');
            }
            
            return result;
        }

        function captureWithEnhancedCanvas() {
            return new Promise((resolve) => {
                try {
                    const waiver = document.querySelector('.waiver-container');
                    if (!waiver) {
                        resolve(null);
                        return;
                    }

                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    
                    canvas.width = waiver.scrollWidth || 800;
                    canvas.height = waiver.scrollHeight || 1200;
                    
                    ctx.fillStyle = '#ffffff';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    
                    ctx.fillStyle = '#000000';
                    ctx.font = '16px Arial';
                    
                    let y = 50;
                    
                    ctx.font = 'bold 20px Arial';
                    ctx.fillText('BICYCLE PROGRAM WAIVER AND RELEASE FROM LIABILITY', 50, y);
                    y += 40;
                    
                    const nameInput = document.querySelector('input[id*="participant_name"]');
                    if (nameInput && nameInput.value) {
                        ctx.font = '16px Arial';
                        ctx.fillText('Participant Name: ' + nameInput.value, 50, y);
                        y += 30;
                    }
                    
                    const agreementCheckbox = document.querySelector('input[id*="agreement"]');
                    if (agreementCheckbox) {
                        ctx.fillText('Agreement: ' + (agreementCheckbox.checked ? '✓ Agreed' : '☐ Not Agreed'), 50, y);
                        y += 30;
                    }
                    
                    ctx.fillText('Date: ' + new Date().toLocaleDateString(), 50, y);
                    y += 40;
                    
                    const sigCanvas = document.getElementById('signature-canvas');
                    if (sigCanvas) {
                        try {
                            ctx.fillText('Signature:', 50, y);
                            y += 20;
                            ctx.drawImage(sigCanvas, 50, y);
                            y += 160;
                        } catch (e) {
                            ctx.fillText('Signature: [Signature Present]', 50, y);
                            y += 30;
                        }
                    }
                    
                    const textContent = waiver.innerText || '';
                    const lines = textContent.split('\n').filter(line => line.trim().length > 0);
                    ctx.font = '12px Arial';
                    
                    lines.slice(0, 50).forEach(line => {
                        if (y < canvas.height - 30) {
                            const words = line.split(' ');
                            let currentLine = '';
                            
                            words.forEach(word => {
                                const testLine = currentLine + word + ' ';
                                const metrics = ctx.measureText(testLine);
                                
                                if (metrics.width > canvas.width - 100) {
                                    ctx.fillText(currentLine, 50, y);
                                    currentLine = word + ' ';
                                    y += 15;
                                } else {
                                    currentLine = testLine;
                                }
                            });
                            
                            if (currentLine.trim().length > 0) {
                                ctx.fillText(currentLine, 50, y);
                                y += 15;
                            }
                        }
                    });
                    
                    resolve(canvas.toDataURL('image/png'));
                } catch (error) {
                    console.error('[JS] Enhanced canvas fallback error:', error);
                    resolve(null);
                }
            });
        }

        Shiny.addCustomMessageHandler('capture_page_screenshot', async () => {
            console.log('[JS] capture_page_screenshot handler called');
            await captureScreenshot();
        });
        
        Shiny.addCustomMessageHandler('hide_submitting_overlay', () => {
            const ov = document.getElementById('submitting-overlay');
            if (ov) ov.style.display = 'none';
        });

        document.addEventListener('DOMContentLoaded', () => {
            loadHtml2Canvas();
        });
        """
    ),
    tags.div(
        ui.output_ui("header_section"),
        ui.output_ui("main_content"),
        ui.tags.footer(
            "Hope's Corner, Inc. Bicycle Program Waiver",
            class_="text-center text-muted small mt-4 py-3",
        ),
        class_="waiver-container",
    ),
    ui.tags.div(
        ui.input_text(
            "page_screenshot",
            None,
            value="",
        ),
        style="display: none;",
    ),
    ui.tags.div(
        ui.tags.div(
            ui.tags.div(
                class_="spinner-border text-light spinner-border-sm", role="status"
            ),
            ui.tags.span("Submitting..."),
            class_="inner",
        ),
        id="submitting-overlay",
    ),
)


def server(input, output, session):
    language = reactive.Value("en")
    is_submitted = reactive.Value(False)
    submitting = reactive.Value(False)
    status_message = reactive.Value("")
    status_type = reactive.Value("info")

    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
    AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
    AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
    SHAREPOINT_SITE_URL = os.getenv("SHAREPOINT_SITE_URL")
    SHAREPOINT_EXCEL_FILE_PATH = os.getenv("SHAREPOINT_EXCEL_FILE_PATH")
    SHAREPOINT_TABLE_NAME = os.getenv("SHAREPOINT_TABLE_NAME")

    def have_graph_config():
        return all(
            [
                AZURE_TENANT_ID,
                AZURE_CLIENT_ID,
                AZURE_CLIENT_SECRET,
                SHAREPOINT_SITE_URL,
                SHAREPOINT_EXCEL_FILE_PATH,
                SHAREPOINT_TABLE_NAME,
            ]
        )

    def graph_token():
        if not have_graph_config():
            return None
        try:
            url = (
                f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/token"
            )
            data = {
                "client_id": AZURE_CLIENT_ID,
                "client_secret": AZURE_CLIENT_SECRET,
                "scope": "https://graph.microsoft.com/.default",
                "grant_type": "client_credentials",
            }
            resp = requests.post(url, data=data, timeout=15)
            resp.raise_for_status()
            return resp.json().get("access_token")
        except Exception as e:
            print(f"[graph] token error: {e}")
            return None

    def site_id(token: str):
        try:
            parsed = urlparse(SHAREPOINT_SITE_URL)
            hostname = parsed.netloc
            site_path = parsed.path.lstrip("/")
            url = f"https://graph.microsoft.com/v1.0/sites/{hostname}:/{site_path}?$select=id"
            r = requests.get(
                url, headers={"Authorization": f"Bearer {token}"}, timeout=15
            )
            r.raise_for_status()
            return r.json()["id"]
        except Exception as e:
            print(f"[graph] site id error: {e}")
            return None

    def ensure_excel_file_exists(token: str, sp_site_id: str):
        try:
            file_path_enc = SHAREPOINT_EXCEL_FILE_PATH.replace(" ", "%20")
            url = f"https://graph.microsoft.com/v1.0/sites/{sp_site_id}/drive/root:/{file_path_enc}"
            r = requests.get(
                url, headers={"Authorization": f"Bearer {token}"}, timeout=20
            )

            if r.status_code == 404:
                print("[graph] Excel file not found, creating new workbook")

                wb = Workbook()
                ws = wb.active
                ws.title = "WaiverData"

                headers = ["Name", "Date", "Language", "Timestamp", "Screenshot_File"]
                for idx, header in enumerate(headers, 1):
                    ws.cell(row=1, column=idx, value=header)

                sample_row = [
                    "Sample Name",
                    "2024-01-01",
                    "en",
                    "2024-01-01 12:00:00",
                    "Sample_Name_20240101_screenshot.png",
                ]
                for idx, value in enumerate(sample_row, 1):
                    ws.cell(row=2, column=idx, value=value)

                from openpyxl.worksheet.table import Table, TableStyleInfo

                tab = Table(displayName=SHAREPOINT_TABLE_NAME, ref="A1:E2")
                style = TableStyleInfo(
                    name="TableStyleMedium2",
                    showFirstColumn=False,
                    showLastColumn=False,
                    showRowStripes=True,
                    showColumnStripes=True,
                )
                tab.tableStyleInfo = style
                ws.add_table(tab)

                from io import BytesIO

                buffer = BytesIO()
                wb.save(buffer)
                buffer.seek(0)

                folder_path = "/".join(SHAREPOINT_EXCEL_FILE_PATH.split("/")[:-1])
                filename = SHAREPOINT_EXCEL_FILE_PATH.split("/")[-1]
                upload_url = f"https://graph.microsoft.com/v1.0/sites/{sp_site_id}/drive/root:/{folder_path.replace(' ', '%20')}/{filename}:/content"

                upload_resp = requests.put(
                    upload_url,
                    headers={"Authorization": f"Bearer {token}"},
                    data=buffer.getvalue(),
                    timeout=30,
                )
                if upload_resp.status_code < 300:
                    print("[graph] Excel file created successfully")
                    return True
                else:
                    print(
                        f"[graph] Failed to create Excel file: {upload_resp.status_code}"
                    )
                    return False
            else:
                print("[graph] Excel file already exists")
                return True
        except Exception as e:
            print(f"[graph] Error ensuring Excel file exists: {e}")
            return False

    def append_excel_row(token: str, sp_site_id: str, waiver_data: dict):
        try:
            if not ensure_excel_file_exists(token, sp_site_id):
                return False

            file_path_enc = SHAREPOINT_EXCEL_FILE_PATH.replace(" ", "%20")
            url = f"https://graph.microsoft.com/v1.0/sites/{sp_site_id}/drive/root:/{file_path_enc}:/workbook/tables/{SHAREPOINT_TABLE_NAME}/rows/add"

            date_obj = datetime.fromisoformat(waiver_data.get("date", ""))
            formatted_date = date_obj.strftime("%Y-%m-%d")

            row_values = [
                waiver_data.get("name", ""),
                formatted_date,
                waiver_data.get("language", ""),
                waiver_data.get("timestamp", ""),
                waiver_data.get("screenshot_filename", ""),
            ]

            body = {"values": [row_values]}
            r = requests.post(
                url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                json=body,
                timeout=20,
            )

            if r.status_code < 300:
                print("[graph] Excel row appended successfully")
                return True
            else:
                session_url = f"https://graph.microsoft.com/v1.0/sites/{sp_site_id}/drive/root:/{file_path_enc}:/workbook/createSession"
                session_resp = requests.post(
                    session_url,
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json",
                    },
                    json={"persistChanges": True},
                    timeout=20,
                )

                if session_resp.status_code < 300:
                    session_id = session_resp.json().get("id")
                    print(f"[graph] Created workbook session: {session_id[:8]}...")

                    table_url = f"https://graph.microsoft.com/v1.0/sites/{sp_site_id}/drive/root:/{file_path_enc}:/workbook/tables/{SHAREPOINT_TABLE_NAME}/rows/add"
                    table_resp = requests.post(
                        table_url,
                        headers={
                            "Authorization": f"Bearer {token}",
                            "Content-Type": "application/json",
                            "workbook-session-id": session_id,
                        },
                        json=body,
                        timeout=20,
                    )

                    if table_resp.status_code < 300:
                        print("[graph] Excel row appended successfully using session")
                        return True
                    else:
                        print(
                            f"[graph] Failed to append Excel row with session: {table_resp.status_code} - {table_resp.text[:200]}"
                        )
                        return False
                else:
                    print(
                        f"[graph] Failed to create workbook session: {session_resp.status_code} - {session_resp.text[:200]}"
                    )
                    return False

                print(
                    f"[graph] Failed to append Excel row: {r.status_code} - {r.text[:200]}"
                )
                return False
        except Exception as e:
            print(f"[graph] Excel append error: {e}")
            return False

    def create_waiver_screenshot(waiver_data, content):
        """Create a server-side screenshot/image of the waiver data"""
        try:
            width = 850
            height = 1600

            img = Image.new("RGB", (width, height), "white")
            draw = ImageDraw.Draw(img)

            try:
                title_font = ImageFont.truetype(
                    "/System/Library/Fonts/Helvetica.ttc", 20
                )
                header_font = ImageFont.truetype(
                    "/System/Library/Fonts/Helvetica.ttc", 16
                )
                normal_font = ImageFont.truetype(
                    "/System/Library/Fonts/Helvetica.ttc", 12
                )
                small_font = ImageFont.truetype(
                    "/System/Library/Fonts/Helvetica.ttc", 10
                )
            except:
                try:
                    title_font = ImageFont.load_default()
                    header_font = ImageFont.load_default()
                    normal_font = ImageFont.load_default()
                    small_font = ImageFont.load_default()
                except:
                    title_font = header_font = normal_font = small_font = None

            y = 30
            margin = 40

            title_text = content["title"]
            if title_font:
                title_lines = textwrap.wrap(title_text, width=50)
                for line in title_lines:
                    draw.text((margin, y), line, fill="black", font=title_font)
                    y += 25
            else:
                draw.text((margin, y), title_text[:80], fill="black")
                y += 25

            y += 20

            draw.text(
                (margin, y),
                content["logo_text1"],
                fill="black",
                font=header_font or title_font,
            )
            y += 20
            draw.text(
                (margin, y),
                content["logo_subtext"],
                fill="black",
                font=normal_font or title_font,
            )
            y += 30

            draw.text(
                (margin, y),
                "FORM SUBMISSION DETAILS:",
                fill="black",
                font=header_font or title_font,
            )
            y += 25

            name_text = f"Participant Name: {waiver_data.get('name', 'N/A')}"
            draw.text(
                (margin, y), name_text, fill="black", font=normal_font or title_font
            )
            y += 20

            agreement_text = f"Agreement Status: {'✓ AGREED' if waiver_data.get('agreement', False) else '☐ NOT AGREED'}"
            draw.text(
                (margin, y),
                agreement_text,
                fill="black",
                font=normal_font or title_font,
            )
            y += 20

            date_text = f"Date: {waiver_data.get('timestamp', 'N/A')}"
            draw.text(
                (margin, y), date_text, fill="black", font=normal_font or title_font
            )
            y += 20

            lang_text = f"Language: {'English' if waiver_data.get('language') == 'en' else 'Spanish'}"
            draw.text(
                (margin, y), lang_text, fill="black", font=normal_font or title_font
            )
            y += 30

            draw.text(
                (margin, y), "SIGNATURE:", fill="black", font=header_font or title_font
            )
            y += 25

            signature_data = waiver_data.get("signature", "")
            if signature_data and signature_data.startswith("data:image"):
                try:
                    header, encoded = signature_data.split(",", 1)
                    signature_bytes = base64.b64decode(encoded)
                    signature_img = Image.open(io.BytesIO(signature_bytes))

                    if signature_img.mode != "RGBA":
                        signature_img = signature_img.convert("RGBA")

                    sig_width = min(400, signature_img.width)
                    sig_height = int(
                        signature_img.height * (sig_width / signature_img.width)
                    )
                    signature_img = signature_img.resize(
                        (sig_width, sig_height), Image.Resampling.LANCZOS
                    )

                    sig_background = Image.new("RGB", (sig_width, sig_height), "white")

                    if signature_img.mode == "RGBA":
                        sig_background.paste(signature_img, (0, 0), signature_img)
                    else:
                        sig_background.paste(signature_img, (0, 0))

                    img.paste(sig_background, (margin, y))
                    y += sig_height + 10
                    print(
                        f"[screenshot] Successfully processed signature: {sig_width}x{sig_height}"
                    )
                except Exception as e:
                    print(f"[screenshot] Could not process signature: {e}")
                    import traceback

                    traceback.print_exc()
                    draw.text(
                        (margin, y),
                        "[Signature Present - Could not display]",
                        fill="black",
                        font=normal_font or title_font,
                    )
                    y += 20
            else:
                draw.text(
                    (margin, y),
                    "[No signature provided]",
                    fill="black",
                    font=normal_font or title_font,
                )
                y += 20

            y += 20

            draw.text(
                (margin, y),
                "WAIVER CONTENT:",
                fill="black",
                font=header_font or title_font,
            )
            y += 25

            intro_lines = textwrap.wrap(content["intro"], width=90)
            for line in intro_lines[:12]:
                draw.text(
                    (margin, y), line, fill="black", font=small_font or normal_font
                )
                y += 12
                if y > height - 150:
                    break

            y += 15

            if y < height - 300:
                for i, point in enumerate(content["points"][:4], 1):
                    point_lines = textwrap.wrap(f"{i}. {point}", width=85)
                    for line in point_lines[:4]:
                        draw.text(
                            (margin, y),
                            line,
                            fill="black",
                            font=small_font or normal_font,
                        )
                        y += 12
                        if y > height - 200:
                            break
                    y += 8
                    if y > height - 200:
                        break

            if y < height - 250:
                sub_points = content.get("sub_points", [])
                for i, sub_point in enumerate(sub_points[:3], 1):
                    sub_lines = textwrap.wrap(f"  • {sub_point}", width=80)
                    for line in sub_lines[:3]:
                        draw.text(
                            (margin + 20, y),
                            line,
                            fill="black",
                            font=small_font or normal_font,
                        )
                        y += 12
                        if y > height - 150:
                            break
                    y += 5
                    if y > height - 150:
                        break

            if y < height - 120:
                y += 15
                draw.text(
                    (margin, y),
                    "IMPORTANT:",
                    fill="black",
                    font=header_font or title_font,
                )
                y += 20
                final_lines = textwrap.wrap(content["final_agreement"], width=85)
                for line in final_lines[:8]:
                    draw.text(
                        (margin, y), line, fill="black", font=small_font or normal_font
                    )
                    y += 12
                    if y > height - 80:
                        break

            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.getvalue()).decode()

            return f"data:image/png;base64,{img_base64}"

        except Exception as e:
            print(f"[screenshot] Error creating waiver screenshot: {e}")
            return None

    def upload_screenshot_with_participant_name(
        token: str, sp_site_id: str, b64data: str, participant_name: str, timestamp: str
    ):
        print("[graph] Starting screenshot upload function")
        print(f"[graph] Data validation - b64data exists: {bool(b64data)}")
        print(
            f"[graph] Data validation - starts with data:image: {b64data.startswith('data:image') if b64data else False}"
        )
        print(f"[graph] Data validation - participant name: '{participant_name}'")
        print(
            f"[graph] Data validation - site_id: '{sp_site_id[:20] if sp_site_id else 'None'}...'"
        )

        if not (b64data and b64data.startswith("data:image")):
            print(
                f"[graph] Screenshot upload failed validation - b64data: {bool(b64data)}, starts with data:image: {b64data.startswith('data:image') if b64data else False}"
            )
            return False
        try:
            import re

            clean_name = re.sub(r"[^\w\s-]", "", participant_name.strip())
            clean_name = re.sub(r"[-\s]+", "_", clean_name)

            folder_path = (
                "/".join(SHAREPOINT_EXCEL_FILE_PATH.split("/")[:-1])
                or "Shared Documents"
            )

            print(f"[graph] SHAREPOINT_EXCEL_FILE_PATH: '{SHAREPOINT_EXCEL_FILE_PATH}'")
            print(f"[graph] Calculated folder_path: '{folder_path}'")

            screenshots_folder = f"{folder_path}/screenshots"
            print(f"[graph] Screenshots folder path: '{screenshots_folder}'")

            create_folder_url = f"https://graph.microsoft.com/v1.0/sites/{sp_site_id}/drive/root:/{folder_path.replace(' ', '%20')}:/children"
            folder_data = {
                "name": "screenshots",
                "folder": {},
                "@microsoft.graph.conflictBehavior": "replace",
            }

            folder_resp = requests.post(
                create_folder_url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                json=folder_data,
                timeout=20,
            )

            if folder_resp.status_code < 300 or folder_resp.status_code == 409:
                print("[graph] Screenshots folder ready for use")
            else:
                print(
                    f"[graph] Screenshots folder creation response: {folder_resp.status_code} - {folder_resp.text[:100]}"
                )

            date_str = datetime.now().strftime("%Y%m%d")
            filename = f"{clean_name}_{date_str}_screenshot.png"

            file_api = f"https://graph.microsoft.com/v1.0/sites/{sp_site_id}/drive/root:/{screenshots_folder.replace(' ', '%20')}/{filename}:/content"

            print(f"[graph] Upload URL: '{file_api}'")

            try:
                header, encoded = b64data.split(",", 1)
                binary = base64.b64decode(encoded)
                print(
                    f"[graph] Successfully decoded base64 data, binary size: {len(binary)} bytes"
                )
            except Exception as decode_error:
                print(f"[graph] Failed to decode base64 data: {decode_error}")
                return False

            print(
                f"[graph] Uploading screenshot to SharePoint: {filename} (size: {len(binary)} bytes)"
            )
            print(f"[graph] Token length: {len(token)} characters")

            try:
                r = requests.put(
                    file_api,
                    headers={"Authorization": f"Bearer {token}"},
                    data=binary,
                    timeout=30,
                )
                print(f"[graph] Upload request completed with status: {r.status_code}")
            except Exception as upload_error:
                print(f"[graph] Upload request failed with exception: {upload_error}")
                return False

            if r.status_code < 300:
                print(f"[graph] Screenshot uploaded: {filename}")
                return f"{screenshots_folder}/{filename}"
            else:
                print(
                    f"[graph] Screenshot upload failed {r.status_code}: {r.text[:120]}"
                )
                return False
        except Exception as e:
            print(f"[graph] Screenshot upload error: {e}")
            return False

    @render.ui
    def header_section():
        content = waiver_content[language.get()]
        return create_header(content, language.get())

    @render.ui
    def main_content():
        if is_submitted.get():
            content = waiver_content[language.get()]
            return ui.tags.div(
                ui.tags.div(
                    ui.tags.div("✓", class_="checkmark"),
                    ui.tags.h3(
                        content["success_message"], class_="h4 fw-bold text-success"
                    ),
                    class_="success-message",
                ),
                ui.tags.script(
                    """
                    // Hide overlay when success page is shown
                    setTimeout(function() {
                        const overlay = document.getElementById('submitting-overlay');
                        if (overlay) overlay.style.display = 'none';
                    }, 100);
                    """
                ),
                class_="p-4",
            )
        else:
            content = waiver_content[language.get()]
            alert = None
            if status_message.get():
                alert = ui.tags.div(
                    status_message.get(),
                    class_=f"alert alert-{status_type.get()} py-2 px-3 mb-3",
                    role="alert",
                )
            return tags.div(
                alert if alert else "",
                create_waiver_content(content),
                create_form_section(content),
                class_="p-4",
            )

    @render.text
    def current_date_display():
        content = waiver_content[language.get()]
        today = datetime.now()
        if language.get() == "en":
            formatted_date = today.strftime("%B %d, %Y")
        else:
            months = [
                "enero",
                "febrero",
                "marzo",
                "abril",
                "mayo",
                "junio",
                "julio",
                "agosto",
                "septiembre",
                "octubre",
                "noviembre",
                "diciembre",
            ]
            formatted_date = f"{today.day} de {months[today.month-1]} de {today.year}"

        return f"{content['date_label']}: {formatted_date}"

    @reactive.Effect
    @reactive.event(input.language_switch)
    def toggle_language():
        current_lang = language.get()
        new_lang = "es" if current_lang == "en" else "en"
        language.set(new_lang)

    @reactive.Effect
    def update_submit_button():
        if (
            hasattr(input, "agreement")
            and hasattr(input, "participant_name")
            and hasattr(input, "signature_data")
        ):
            if (
                input.agreement()
                and input.participant_name()
                and input.signature_data()
            ):
                ui.update_action_button("submit_waiver", disabled=False)
            else:
                ui.update_action_button("submit_waiver", disabled=True)

    @reactive.Effect
    async def inject_html2canvas():
        await session.send_custom_message("inject_html2canvas", {})

    @reactive.Effect
    @reactive.event(input.submit_waiver)
    async def submit_waiver():
        if not (
            input.agreement() and input.participant_name() and input.signature_data()
        ):
            await session.send_custom_message("hide_submitting_overlay", {})
            return
        if submitting.get():
            await session.send_custom_message("hide_submitting_overlay", {})
            return

        print("[submit] Starting waiver submission...")

        submitting.set(True)
        ui.update_action_button(
            "submit_waiver",
            label=("Submitting..." if language.get() == "en" else "Enviando..."),
            disabled=True,
        )

        today = datetime.now()
        screenshot_data = ""

        print("[submit] Generating server-side screenshot...")

        current_lang = language.get()
        current_content = waiver_content[current_lang]

        waiver_form_data = {
            "name": input.participant_name(),
            "agreement": True,
            "signature": input.signature_data(),
            "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
            "language": language.get(),
        }

        screenshot_data = create_waiver_screenshot(waiver_form_data, current_content)

        if screenshot_data:
            print(
                f"[submit] Generated server-side screenshot: {len(screenshot_data)} bytes"
            )
        else:
            print("[submit] Failed to generate server-side screenshot")
            screenshot_data = None

        clean_name = input.participant_name().strip()
        import re

        clean_name = re.sub(r"[^\w\s-]", "", clean_name)
        clean_name = re.sub(r"[-\s]+", "_", clean_name)
        date_str = today.strftime("%Y%m%d")
        screenshot_filename = f"{clean_name}_{date_str}_screenshot.png"

        waiver_data = {
            "name": input.participant_name(),
            "signature": input.signature_data(),
            "date": today.isoformat(),
            "language": language.get(),
            "timestamp": today.strftime("%Y-%m-%d %H:%M:%S"),
            "screenshot": screenshot_data,
            "screenshot_filename": screenshot_filename,
        }

        if not have_graph_config():
            print("[graph] SharePoint configuration is missing")
            status_message.set(
                "SharePoint configuration error. Cannot save waiver."
                if language.get() == "en"
                else "Error de configuración de SharePoint. No se puede guardar la renuncia."
            )
            status_type.set("danger")
            is_submitted.set(False)
            submitting.set(False)
            await session.send_custom_message("hide_submitting_overlay", {})
            return

        if have_graph_config():
            try:
                token = graph_token()
                if token:
                    sid = site_id(token)
                    if sid:
                        excel_success = append_excel_row(token, sid, waiver_data)
                        if not excel_success:
                            print("[graph] Failed to append data to Excel.")
                            status_message.set(
                                "Failed to save waiver to SharePoint Excel."
                                if language.get() == "en"
                                else "Error al guardar la renuncia en Excel de SharePoint."
                            )
                            status_type.set("danger")
                        else:
                            print("[graph] Successfully appended data to Excel.")

                        if waiver_data.get("screenshot"):
                            print(
                                f"[graph] About to upload screenshot for {waiver_data['name']}, data size: {len(waiver_data['screenshot'])}"
                            )
                            print(
                                f"[graph] Screenshot data preview: {waiver_data['screenshot'][:50]}..."
                            )
                            screenshot_path = upload_screenshot_with_participant_name(
                                token,
                                sid,
                                waiver_data["screenshot"],
                                waiver_data["name"],
                                waiver_data["timestamp"],
                            )
                            if screenshot_path:
                                print(f"[graph] Screenshot saved to: {screenshot_path}")
                            else:
                                print(
                                    "[graph] Failed to upload screenshot to SharePoint"
                                )
                        else:
                            print("[graph] No screenshot data to upload")
                            print(
                                f"[graph] Waiver data keys: {list(waiver_data.keys())}"
                            )
                            if waiver_data.get("screenshot") == "":
                                print("[graph] Screenshot data is empty string")
                    else:
                        print("[graph] Failed to get SharePoint site ID")
                        status_message.set(
                            "Failed to connect to SharePoint site."
                            if language.get() == "en"
                            else "Error al conectar con el sitio de SharePoint."
                        )
                        status_type.set("danger")
                        await session.send_custom_message("hide_submitting_overlay", {})
                else:
                    print("[graph] Failed to get Microsoft Graph token")
                    status_message.set(
                        "SharePoint authentication failed."
                        if language.get() == "en"
                        else "Error de autenticación con SharePoint."
                    )
                    status_type.set("danger")
                    await session.send_custom_message("hide_submitting_overlay", {})
            except Exception as e:
                print(f"[graph] SharePoint submission error: {e}")
                status_message.set(
                    "Error connecting to SharePoint."
                    if language.get() == "en"
                    else "Error al conectar con SharePoint."
                )
                status_type.set("danger")
                await session.send_custom_message("hide_submitting_overlay", {})

        is_submitted.set(True)
        submitting.set(False)
        status_message.set(
            "Waiver submitted successfully!"
            if language.get() == "en"
            else "¡Renuncia enviada con éxito!"
        )
        status_type.set("success")
        print(f"Waiver submitted - Participant: {waiver_data['name']}")
        await session.send_custom_message("hide_submitting_overlay", {})


app = App(app_ui, server)
