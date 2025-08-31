from shiny import App, ui, render, reactive
import htmltools as tags
from datetime import datetime
import os
import requests
from urllib.parse import urlparse
import base64
from openpyxl import Workbook

try:
    from dotenv import load_dotenv  # type: ignore

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
            class_="bg-success text-white p-4 position-relative",
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
            # Agreement checkbox
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
                        // Trigger change event for Shiny
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
        
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(function() {
                const submitButton = document.querySelector('button[id*="submit_waiver"]');
                if (submitButton) {
                    console.log('[JS] Found submit button, adding screenshot capture listener');
                    submitButton.addEventListener('click', function(event) {
                        console.log('[JS] Submit button clicked - capturing screenshot immediately');
                        
                        if (window.html2canvas) {
                            captureScreenshot().then(() => {
                            }).catch(() => {
                            });
                        } else {
                        }
                    }, true);
                } else {
                }
            }, 1000);
        });
        """
    ),
    ui.tags.script(
        """
        document.addEventListener('DOMContentLoaded', function() {
            if (!window.html2canvas && !window._html2canvasLoading) {
                console.log('[JS] Loading html2canvas library on page load...');
                window._html2canvasLoading = true;
                const s = document.createElement('script');
                s.src = 'https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js';
                s.onload = () => { 
                    window._html2canvasLoaded = true; 
                    console.log('[JS] html2canvas loaded successfully on page load');
                };
                s.onerror = () => {
                    console.error('[JS] Failed to load html2canvas on page load');
                    window._html2canvasLoading = false;
                };
                document.head.appendChild(s);
            }
        });
        
        Shiny.addCustomMessageHandler('inject_html2canvas', function() {
            if (window._html2canvasLoading || window.html2canvas) {
                console.log('[JS] html2canvas already loaded or loading');
                return;
            }
            console.log('[JS] Loading html2canvas library on demand...');
            window._html2canvasLoading = true;
            const s = document.createElement('script');
            s.src = 'https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js';
            s.onload = () => { 
                window._html2canvasLoaded = true; 
                console.log('[JS] html2canvas loaded successfully on demand');
            };
            s.onerror = () => {
                console.error('[JS] Failed to load html2canvas on demand');
                window._html2canvasLoading = false;
            };
            document.head.appendChild(s);
        });
        Shiny.addCustomMessageHandler('capture_page_screenshot', async function() {
            const timestamp = new Date().toLocaleTimeString();
            console.log(`[JS] ${timestamp} - Screenshot capture handler called`);
            console.log('[JS] html2canvas available:', !!window.html2canvas);
            console.log('[JS] Document ready state:', document.readyState);
            console.log('[JS] Current page scroll:', window.pageYOffset);
            
            if (document.readyState !== 'complete') {
                console.log('[JS] Document not ready, waiting...');
                setTimeout(() => {
                    Shiny.addCustomMessageHandler('capture_page_screenshot')();
                }, 500);
                return;
            }
            
            if (!window.html2canvas) { 
                console.error('[JS] html2canvas not loaded - attempting to load now');
                // Try to load it immediately
                const script = document.createElement('script');
                script.src = 'https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js';
                script.onload = function() {
                    console.log('[JS] html2canvas loaded successfully, retrying capture');
                    // Retry the capture after a brief delay
                    setTimeout(() => captureScreenshot(), 300);
                };
                script.onerror = function() {
                    console.error('[JS] Failed to load html2canvas');
                };
                document.head.appendChild(script);
                return; 
            }
            
            setTimeout(() => captureScreenshot(), 200);
        });
        
        async function captureScreenshot() {
            console.log('[JS] Starting screenshot capture...');
            
            if (!window.html2canvas) {
                console.error('[JS] html2canvas still not available in captureScreenshot');
                return;
            }
            
            try {
                let targetElement = document.querySelector('.waiver-container');
                if (!targetElement) {
                    targetElement = document.body;
                    console.log('[JS] Waiver container not found, using body');
                } else {
                    console.log('[JS] Found waiver container, capturing specific element');
                }
                
                console.log('[JS] Target element:', targetElement);
                console.log('[JS] Target element scroll height:', targetElement.scrollHeight);
                console.log('[JS] Target element client height:', targetElement.clientHeight);
                
                window.scrollTo(0, 0);
                
                await new Promise(resolve => setTimeout(resolve, 500));
                
                const agreementCheckbox = document.querySelector('input[type="checkbox"]') || 
                                        document.querySelector('input[id*="agreement"]');
                const nameInput = document.querySelector('input[type="text"]') || 
                                document.querySelector('input[id*="participant_name"]');
                const signatureCanvas = document.getElementById('signature-canvas');
                
                console.log('[JS] Form state check:');
                console.log('  - Agreement checked:', agreementCheckbox ? agreementCheckbox.checked : 'not found');
                console.log('  - Name filled:', nameInput ? (nameInput.value ? 'yes' : 'no') : 'not found');
                console.log('  - Name input ID:', nameInput ? nameInput.id : 'not found');
                console.log('  - Agreement ID:', agreementCheckbox ? agreementCheckbox.id : 'not found');
                console.log('  - Signature canvas:', signatureCanvas ? 'found' : 'not found');
                
                const captureOptions = {
                    scale: 1.2,
                    useCORS: true,
                    allowTaint: false,
                    backgroundColor: '#f8f9fa',
                    logging: false,
                    ignoreElements: function(element) {
                        return element.style.display === 'none' || 
                               element.id === 'page_screenshot' || 
                               element.id === 'signature_data';
                    }
                };
                
                if (targetElement.classList.contains('waiver-container')) {
                    captureOptions.height = targetElement.scrollHeight;
                    captureOptions.width = Math.max(targetElement.scrollWidth, 800);
                } else {
                    captureOptions.height = Math.max(document.body.scrollHeight, window.innerHeight);
                    captureOptions.width = window.innerWidth;
                }
                
                console.log('[JS] Capture dimensions:', captureOptions.width, 'x', captureOptions.height);
                
                const canvas = await html2canvas(targetElement, captureOptions);
                
                console.log('[JS] Canvas created:', canvas.width, 'x', canvas.height);
                
                const dataURL = canvas.toDataURL('image/png');
                console.log('[JS] DataURL created, length:', dataURL.length);
                
                const input = document.getElementById('page_screenshot');
                console.log('[JS] Input element found:', !!input);
                console.log('[JS] Input element type:', input ? input.type : 'N/A');
                console.log('[JS] Input element name:', input ? input.name : 'N/A');
                console.log('[JS] Input current value length:', input ? input.value.length : 0);
                
                if (input) { 
                    input.value = dataURL; 
                    console.log('[JS] Input value set, length:', input.value.length);
                    
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true })); 
                    
                    if (window.Shiny && window.Shiny.setInputValue) {
                        console.log('[JS] Also setting via Shiny.setInputValue');
                        Shiny.setInputValue('page_screenshot', dataURL, {priority: 'event'});
                    }
                    
                    input.focus();
                    input.blur();
                    
                    console.log('[JS] Screenshot captured and saved to input field successfully');
                    
                    
                    setTimeout(() => {
                        console.log('[JS] Verification - input value length after 100ms:', input.value.length);
                    }, 100);
                    
                } else {
                    console.error('[JS] page_screenshot input element not found');
                }
            } catch (e) { 
                console.error('[JS] Screenshot capture failed:', e); 
            }
        }
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
                
                sample_row = ["Sample Name", "2024-01-01", "en", "2024-01-01 12:00:00", "Sample_Name_20240101_screenshot.png"]
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
                        "Content-Type": "application/json"
                    },
                    json={"persistChanges": True},
                    timeout=20
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
                            "workbook-session-id": session_id
                        },
                        json=body,
                        timeout=20
                    )
                    
                    if table_resp.status_code < 300:
                        print("[graph] Excel row appended successfully using session")
                        return True
                    else:
                        print(f"[graph] Failed to append Excel row with session: {table_resp.status_code} - {table_resp.text[:200]}")
                        return False
                else:
                    print(f"[graph] Failed to create workbook session: {session_resp.status_code} - {session_resp.text[:200]}")
                    return False
                    
                print(f"[graph] Failed to append Excel row: {r.status_code} - {r.text[:200]}")
                return False
        except Exception as e:
            print(f"[graph] Excel append error: {e}")
            return False

    def upload_screenshot_with_participant_name(
        token: str, sp_site_id: str, b64data: str, participant_name: str, timestamp: str
    ):
        print("[graph] Starting screenshot upload function")
        print(f"[graph] Data validation - b64data exists: {bool(b64data)}")
        print(f"[graph] Data validation - starts with data:image: {b64data.startswith('data:image') if b64data else False}")
        print(f"[graph] Data validation - participant name: '{participant_name}'")
        print(f"[graph] Data validation - site_id: '{sp_site_id[:20] if sp_site_id else 'None'}...'")
        
        if not (b64data and b64data.startswith("data:image")):
            print(f"[graph] Screenshot upload failed validation - b64data: {bool(b64data)}, starts with data:image: {b64data.startswith('data:image') if b64data else False}")
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
                "@microsoft.graph.conflictBehavior": "replace"
            }
            
            folder_resp = requests.post(
                create_folder_url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json=folder_data,
                timeout=20
            )
            
            if folder_resp.status_code < 300 or folder_resp.status_code == 409:
                print("[graph] Screenshots folder ready for use")
            else:
                print(f"[graph] Screenshots folder creation response: {folder_resp.status_code} - {folder_resp.text[:100]}")

            date_str = datetime.now().strftime("%Y%m%d")
            filename = f"{clean_name}_{date_str}_screenshot.png"

            file_api = f"https://graph.microsoft.com/v1.0/sites/{sp_site_id}/drive/root:/{screenshots_folder.replace(' ', '%20')}/{filename}:/content"
            
            print(f"[graph] Upload URL: '{file_api}'")

            try:
                header, encoded = b64data.split(",", 1)
                binary = base64.b64decode(encoded)
                print(f"[graph] Successfully decoded base64 data, binary size: {len(binary)} bytes")
            except Exception as decode_error:
                print(f"[graph] Failed to decode base64 data: {decode_error}")
                return False
            
            print(f"[graph] Uploading screenshot to SharePoint: {filename} (size: {len(binary)} bytes)")
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

    @output
    @render.ui
    def header_section():
        content = waiver_content[language.get()]
        return create_header(content, language.get())

    @output
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
        # Load html2canvas as soon as the app starts
        await session.send_custom_message("inject_html2canvas", {})

    

    @reactive.Effect
    @reactive.event(input.submit_waiver)
    async def submit_waiver():
        import asyncio
        
        if not (
            input.agreement() and input.participant_name() and input.signature_data()
        ):
            return
        if submitting.get():
            return

        print("[submit] Checking for existing screenshot data...")
        current_screenshot_length = len(input.page_screenshot()) if hasattr(input, 'page_screenshot') and input.page_screenshot() else 0
        print(f"[submit] Current page_screenshot value length: {current_screenshot_length}")
        
        if current_screenshot_length == 0:
            await session.send_custom_message("capture_page_screenshot", {})
            
            screenshot_captured = False
            for attempt in range(15):  # Wait up to 7.5 seconds
                await asyncio.sleep(0.5)
                current_length = len(input.page_screenshot()) if hasattr(input, "page_screenshot") and input.page_screenshot() else 0
                if current_length > 0:
                    print(f"[submit] Screenshot captured successfully, size: {current_length}")
                    screenshot_captured = True
                    break
                print(f"[submit] Waiting for screenshot, attempt {attempt + 1}")
            
            if not screenshot_captured:
                print("[submit] Screenshot capture failed, proceeding without screenshot")
        else:
            print(f"[submit] Using existing screenshot data, size: {current_screenshot_length}")

        submitting.set(True)
        ui.update_action_button(
            "submit_waiver",
            label=("Submitting..." if language.get() == "en" else "Enviando..."),
            disabled=True,
        )

        today = datetime.now()
        screenshot_data = ""
        
        print("[submit] Checking for screenshot data...")
        print(f"[submit] hasattr(input, 'page_screenshot'): {hasattr(input, 'page_screenshot')}")
        if hasattr(input, "page_screenshot"):
            raw_screenshot = input.page_screenshot()
            print(f"[submit] input.page_screenshot() exists: {bool(raw_screenshot)}")
            print(f"[submit] input.page_screenshot() length: {len(raw_screenshot) if raw_screenshot else 0}")
            if raw_screenshot:
                print(f"[submit] Screenshot data preview: {raw_screenshot[:50]}...")
                screenshot_data = raw_screenshot
        else:
            print("[submit] No page_screenshot attribute on input object")
            
        if not screenshot_data:
            print("[submit] No screenshot data available for upload")
            
 
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
                            print(f"[graph] About to upload screenshot for {waiver_data['name']}, data size: {len(waiver_data['screenshot'])}")
                            print(f"[graph] Screenshot data preview: {waiver_data['screenshot'][:50]}...")
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
                                print("[graph] Failed to upload screenshot to SharePoint")
                        else:
                            print("[graph] No screenshot data to upload")
                            print(f"[graph] Waiver data keys: {list(waiver_data.keys())}")
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
                else:
                    print("[graph] Failed to get Microsoft Graph token")
                    status_message.set(
                        "SharePoint authentication failed."
                        if language.get() == "en"
                        else "Error de autenticación con SharePoint."
                    )
                    status_type.set("danger")
            except Exception as e:
                print(f"[graph] SharePoint submission error: {e}")
                status_message.set(
                    "Error connecting to SharePoint."
                    if language.get() == "en"
                    else "Error al conectar con SharePoint."
                )
                status_type.set("danger")

        is_submitted.set(True)
        submitting.set(False)
        status_message.set(
            "Waiver submitted successfully!"
            if language.get() == "en"
            else "¡Renuncia enviada con éxito!"
        )
        status_type.set("success")
        print(f"Waiver submitted - Participant: {waiver_data['name']}")


app = App(app_ui, server)
