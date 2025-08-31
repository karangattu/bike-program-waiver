import React, { useState, useEffect, useRef } from 'react';
import html2canvas from 'html2canvas';

const waiverContent = {
  en: {
    title: "BICYCLE PROGRAM WAIVER AND RELEASE FROM LIABILITY",
    logoText1: "HOPE'S CORNER",
    logoSubtext: "SHARING MEALS, BUILDING COMMUNITY",
    intro: "I expressly assume and accept any and all risk of injury or death to myself or others arising from my use of the Hope's Corner, Inc. Bicycle Program including repair services, transportation equipment such as bicycles, scooters, skateboards, etc. and all equipment and supplies. This waiver and release from liability includes any and all repair services, equipment, including but not limited to, the bicycle, helmet, lock, light, rack, basket, tubes, tires, chains, brakes, and my participation in the Program.",
    points: [
      "I am a voluntary participant and utilize the program services and equipment at my own risk.",
      "I am responsible for maintaining the bicycle in good condition. I will inspect the bicycle prior to use to ensure all parts are in proper working condition.",
      "I understand that there are risks inherent in riding a bicycle even when the bicycle and equipment are in good working order and used properly. Injuries are a common, ordinary and foreseeable consequence of bicycle riding. I understand that the risks I may encounter include, but are not limited to the following:",
    ],
    subPoints: [
        "The equipment may break or malfunction, causing loss of or damage to property or injury to my person or to another person.",
        "Riding a bicycle requires physical exertion and may result in discomfort, pain or injury.",
        "I might encounter hazards while riding which could cause me to fall or be propelled.",
        "Bicycle travel is dangerous. I may be injured by many factors over which I have no control."
    ],
    volunteerClause: "I understand that I assume the risk of any damage or failure of equipment arising from repair work or services donated to me by the Bicycle Program volunteers, employees or vendors. I understand the program volunteers and employees are not trained or licensed professionals and cannot be held responsible for damage to my equipment. I am responsible for inspecting the work and not utilizing the bicycle or equipment if it is not in good working order.",
    indemnifyClause: "I agree to indemnify, defend, save and hold harmless Hope's Corner, Inc. including all employees, volunteers, directors, officers, vendors and funders of the program from any claims, losses, damages or liability accruing or resulting to any person or entity from my participation in the Bicycle Program or use of the bicycle, bicycle equipment and bicycle repair services.",
    releaseClause: "I, on behalf of myself, my heirs, successors and assigns, hereby waive, release and forever discharge Hope's Corner, Inc. including all employees, volunteers, directors, officers, vendors and funders of the program from any and all claims, losses, damages or liability accruing or resulting to any person or entity from my participation in the Bicycle Program or use of the bicycle, bicycle equipment and repair services.",
    finalAgreement: "I AM AWARE THAT THIS IS A RELEASE OF LIABILITY. I AM SIGNING IT FREELY AND OF MY OWN ACCORD AND I RECOGNIZE AND AGREE THAT IT IS BINDING UPON MYSELF, MY HEIRS AND ASSIGNS, AND IN THE EVENT THAT I AM SIGNING IT ON BEHALF OF ANY MINORS, I HAVE FULL LEGAL AUTHORITY TO DO SO, AND REALIZE THE BINDING EFFECT OF THIS CONTRACT ON THEM, AS WELL AS ON MYSELF. I AGREE TO ALLOW HOPE'S CORNER, INC. TO USE PHOTOGRAPHS, VIDEOS, OR SOUND RECORDINGS OF ME FOR PROMOTIONAL AND PUBLICITY PURPOSES.",
    agreementCheck: "I have carefully read this agreement and understand that this is a release of liability. I agree to the terms and conditions.",
    printNameLabel: "Print Full Name",
  signatureLabel: "Signature (Draw below)",
  clearSignatureButton: "Clear",
    dateLabel: "Date",
    submitButton: "Submit Waiver",
    switchButton: "Leer en Español",
    successMessage: "Thank you! Your waiver has been submitted successfully.",
  },
  es: {
    title: "PROGRAMA DE BICICLETAS ACUERDO DE RENUNCIA Y EXENCIÓN DE RESPONSABILIDAD",
    logoText1: "HOPE'S CORNER",
    logoSubtext: "COMPARTIR COMIDAS, CONSTRUYENDO COMUNIDAD",
    intro: "Asumo y acepto expresamente todos y cada uno de los riesgos de lesiones o muerte para mí u otros que surjan de mi uso del Programa de Bicicletas de Hope's Corner, Inc., incluidos los servicios de reparación, equipos de transporte como bicicletas, scooters, patinetas, etc., y todo el equipo y los suministros. Esta renuncia y exención de responsabilidad incluye todos y cada uno de los servicios de reparación, equipos, incluidos, entre otros, la bicicleta, el casco, el candado, la luz, el portabultos, la canasta, las cámaras, los neumáticos, las cadenas, los frenos y mi participación en el Programa.",
    points: [
      "Soy un participante voluntario y utilizo los servicios y el equipo del programa bajo mi propio riesgo.",
      "Soy responsable de mantener la bicicleta en buenas condiciones. Inspeccionaré la bicicleta antes de usarla para asegurarme de que todas las piezas estén en condiciones de funcionamiento adecuadas.",
      "Entiendo que existen riesgos inherentes al andar en bicicleta incluso cuando la bicicleta y el equipo están en buen estado de funcionamiento y se utilizan correctamente. Las lesiones son una consecuencia común, ordinaria y previsible de andar en bicicleta. Entiendo que los riesgos que puedo encontrar incluyen, entre otros, los siguientes:",
    ],
    subPoints: [
        "El equipo puede romperse o funcionar mal, causando pérdidas o daños a la propiedad o lesiones a mi persona o a otra persona.",
        "Andar en bicicleta requiere esfuerzo físico y puede provocar molestias, dolor o lesiones.",
        "Podría encontrar peligros mientras conduzco que podrían hacer que me caiga o sea impulsado.",
        "Viajar en bicicleta es peligroso. Puedo resultar herido por muchos factores sobre los que no tengo control."
    ],
    volunteerClause: "Entiendo que asumo el riesgo de cualquier daño o falla del equipo que surja del trabajo de reparación o los servicios que me donen los voluntarios, empleados o proveedores del Programa de Bicicletas. Entiendo que los voluntarios y empleados del programa no son profesionales capacitados o con licencia y no se les puede hacer responsables de los daños a mi equipo. Soy responsable de inspeccionar el trabajo y no utilizar la bicicleta o el equipo si no está en buen estado de funcionamiento.",
    indemnifyClause: "Acepto indemnizar, defender, salvar y mantener indemne a Hope's Corner, Inc., incluidos todos los empleados, voluntarios, directores, funcionarios, proveedores y financiadores del programa de cualquier reclamo, pérdida, daño o responsabilidad que se acumule o resulte para cualquier persona o entidad de mi participación en el Programa de Bicicletas o el uso de la bicicleta, el equipo de la bicicleta y los servicios de reparación de bicicletas.",
    releaseClause: "Yo, en mi nombre, mis herederos, sucesores y cesionarios, por la presente renuncio, libero y descargo para siempre a Hope's Corner, Inc., incluidos todos los empleados, voluntarios, directores, funcionarios, proveedores y financiadores del programa de cualquier y todos los reclamos, pérdidas, daños o responsabilidad que se acumulen o resulten para cualquier persona o entidad de mi participación en el Programa de Bicicletas o el uso de la bicicleta, el equipo de la bicicleta y los servicios de reparación.",
    finalAgreement: "SOY CONSCIENTE DE QUE ESTA ES UNA EXENCIÓN DE RESPONSABILIDAD. LO FIRMO LIBREMENTE Y POR MI PROPIA VOLUNTAD Y RECONOZCO Y ACEPTO QUE ES VINCULANTE PARA MÍ, MIS HEREDEROS Y CESIONARIOS, Y EN CASO DE QUE LO FIRME EN NOMBRE DE MENORES, TENGO PLENA AUTORIDAD LEGAL PARA HACERLO, Y ME DOY CUENTA DEL EFECTO VINCULANTE DE ESTE CONTRATO SOBRE ELLOS, ASÍ COMO SOBRE MÍ. ACEPTO PERMITIR QUE HOPE'S CORNER, INC. UTILICE FOTOGRAFÍAS, VIDEOS O GRABACIONES DE SONIDO DE MÍ PARA FINES PROMOCIONALES Y PUBLICITARIOS.",
    agreementCheck: "He leído atentamente este acuerdo y entiendo que se trata de una exención de responsabilidad. Acepto los términos y condiciones.",
    printNameLabel: "Escriba el Nombre Completo",
  signatureLabel: "Firma (Dibuje abajo)",
  clearSignatureButton: "Limpiar",
    dateLabel: "Fecha",
    submitButton: "Enviar Renuncia",
    switchButton: "Read in English",
    successMessage: "¡Gracias! Su renuncia ha sido enviada con éxito.",
  }
};

export default function App() {
  const [language, setLanguage] = useState('en');
  const [formData, setFormData] = useState({ name: '' });
  const [signatureImage, setSignatureImage] = useState('');
  const [agreed, setAgreed] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [currentDate, setCurrentDate] = useState('');
  const canvasRef = useRef(null);
  const drawing = useRef(false);
  const lastPoint = useRef({ x: 0, y: 0 });

  useEffect(() => {
    const today = new Date();
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    setCurrentDate(today.toLocaleDateString(language === 'en' ? 'en-US' : 'es-ES', options));
  }, [language]);

  const handleLanguageSwitch = () => {
    setLanguage(language === 'en' ? 'es' : 'en');
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };
  
  const pageRef = useRef(null);

  const captureScreenshot = async () => {
    if (!pageRef.current) return;
    const canvas = await html2canvas(pageRef.current, { scale: 2, useCORS: true });
    const dataUrl = canvas.toDataURL('image/png');
    const link = document.createElement('a');
    link.href = dataUrl;
    link.download = `waiver_${Date.now()}.png`;
    link.click();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (agreed && formData.name && signatureImage) {
      await captureScreenshot();
      setIsSubmitted(true);
      console.log("Waiver Submitted:", { ...formData, agreed, date: currentDate, language, signatureImage });
    } else {
      alert(language === 'en' ? 'Please complete all required fields and provide a valid signature.' : 'Complete todos los campos requeridos y proporcione una firma válida.');
    }
  };

  const content = waiverContent[language];
  const isFormValid = agreed && formData.name.trim() !== '' && signatureImage;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const resize = () => {
      const ratio = window.devicePixelRatio || 1;
      const rect = canvas.getBoundingClientRect();
      canvas.width = rect.width * ratio;
      canvas.height = 180 * ratio;
      canvas.style.height = '180px';
      const ctx = canvas.getContext('2d');
      ctx.scale(ratio, ratio);
      ctx.lineJoin = 'round';
      ctx.lineCap = 'round';
      ctx.strokeStyle = '#111827';
      ctx.lineWidth = 2;
      if (signatureImage) {
        const img = new Image();
        img.onload = () => ctx.drawImage(img, 0, 0, rect.width, 180);
        img.src = signatureImage;
      }
    };
    resize();
    window.addEventListener('resize', resize);
    return () => window.removeEventListener('resize', resize);
  }, [signatureImage]);

  const pointerPos = (e) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    return { x: clientX - rect.left, y: clientY - rect.top };
  };

  const startDraw = (e) => {
    drawing.current = true;
    lastPoint.current = pointerPos(e);
  };

  const draw = (e) => {
    if (!drawing.current) return;
    e.preventDefault();
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const current = pointerPos(e);
    ctx.beginPath();
    ctx.moveTo(lastPoint.current.x, lastPoint.current.y);
    ctx.lineTo(current.x, current.y);
    ctx.stroke();
    lastPoint.current = current;
  };

  const endDraw = () => {
    if (!drawing.current) return;
    drawing.current = false;
    const canvas = canvasRef.current;
    setSignatureImage(canvas.toDataURL('image/png'));
  };

  const clearSignature = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    setSignatureImage('');
  };

  return (
    <div className="bg-gray-100 min-h-screen font-sans antialiased text-gray-800">
      <div className="container mx-auto p-4 sm:p-6 lg:p-8 max-w-4xl">
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <header className="bg-green-900 text-white p-6 relative">
             <div className="absolute top-4 right-4">
              <button
                onClick={handleLanguageSwitch}
                className="bg-white text-green-800 font-semibold py-2 px-4 rounded-full shadow-md hover:bg-gray-200 transition duration-300 ease-in-out text-sm"
              >
                {content.switchButton}
              </button>
            </div>
            <div className="text-center">
                 <img src="https://images.squarespace-cdn.com/content/v1/5622cd82e4b0501d40689558/cdab4aef-0027-40b7-9737-e2f893586a6a/Hopes_Corner_Logo_Green.png?format=500w" alt="Hope's Corner Logo" className="mx-auto mb-4 h-20 object-contain bg-white/95 p-2 rounded-md shadow-sm" />
                 <h1 className="text-xl sm:text-2xl font-bold">{content.logoText1}</h1>
                 <h2 className="text-3xl sm:text-4xl font-extrabold tracking-wider">{content.logoText2}</h2>
                 <p className="text-sm font-light mt-1">{content.logoSubtext}</p>
            </div>
          </header>

          <main className="p-6 sm:p-8">
            {isSubmitted ? (
              <div className="text-center p-12 bg-green-50 rounded-lg">
                <svg className="mx-auto h-16 w-16 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <h3 className="mt-4 text-2xl font-bold text-gray-900">{content.successMessage}</h3>
              </div>
            ) : (
              <form onSubmit={handleSubmit}>
                <h3 className="text-xl sm:text-2xl font-bold text-center mb-6">{content.title}</h3>
                <div className="space-y-4 text-sm sm:text-base leading-relaxed">
                    <p>{content.intro}</p>
                    <ul className="list-decimal list-inside space-y-2 pl-2">
                        <li>{content.points[0]}</li>
                        <li>{content.points[1]}</li>
                        <li>{content.points[2]}
                            <ul className="list-[lower-alpha] list-inside space-y-1 mt-2 pl-4">
                                <li>{content.subPoints[0]}</li>
                                <li>{content.subPoints[1]}</li>
                                <li>{content.subPoints[2]}</li>
                                <li>{content.subPoints[3]}</li>
                            </ul>
                        </li>
                    </ul>
                    <p>{content.volunteerClause}</p>
                    <p>{content.indemnifyClause}</p>
                    <p>{content.releaseClause}</p>
                    <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-r-lg">
                        <p className="font-bold text-sm uppercase tracking-wide">{content.finalAgreement}</p>
                    </div>
                </div>

                <div className="mt-8 pt-6 border-t border-gray-200">
                  <div className="space-y-6">
                    <div className="relative flex items-start">
                      <div className="flex items-center h-5">
                        <input
                          id="agreement"
                          name="agreement"
                          type="checkbox"
                          checked={agreed}
                          onChange={(e) => setAgreed(e.target.checked)}
                          className="focus:ring-blue-500 h-5 w-5 text-blue-600 border-gray-300 rounded"
                        />
                      </div>
                      <div className="ml-3 text-sm">
                        <label htmlFor="agreement" className="font-medium text-gray-700">{content.agreementCheck}</label>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">{content.printNameLabel}</label>
                        <input type="text" name="name" id="name" value={formData.name} onChange={handleInputChange} className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm" required />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">{content.signatureLabel}</label>
                        <div className="relative border border-gray-300 rounded-md bg-white overflow-hidden select-none">
                          <canvas
                            ref={canvasRef}
                            className="w-full h-44 touch-none"
                            onMouseDown={startDraw}
                            onMouseMove={draw}
                            onMouseUp={endDraw}
                            onMouseLeave={endDraw}
                            onTouchStart={startDraw}
                            onTouchMove={draw}
                            onTouchEnd={endDraw}
                          />
                          {!signatureImage && <div className="absolute inset-0 flex items-center justify-center pointer-events-none text-gray-400 text-xs">{language==='en'?'Sign here':'Firme aquí'}</div>}
                        </div>
                        <div className="flex justify-between mt-2">
                          <button type="button" onClick={clearSignature} className="text-xs px-3 py-1 rounded-full border border-gray-300 hover:bg-gray-100 transition">{content.clearSignatureButton}</button>
                          {signatureImage && <span className="text-xs text-green-600">✓</span>}
                        </div>
                      </div>
                    </div>
                    
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">{content.dateLabel}</label>
                        <p className="block w-full px-3 py-2 bg-gray-100 border border-gray-300 rounded-md shadow-sm sm:text-sm">{currentDate}</p>
                    </div>

                    <div className="text-right">
                      <button
                        type="submit"
                        disabled={!isFormValid}
                        className="inline-flex justify-center py-3 px-8 border border-transparent shadow-sm text-base font-medium rounded-full text-white bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                      >
                        {content.submitButton}
                      </button>
                    </div>
                  </div>
                </div>
              </form>
            )}
          </main>
        </div>
        <footer className="text-center text-xs text-gray-500 mt-4">
          Hope's Corner, Inc. Bicycle Program Waiver
        </footer>
      </div>
    </div>
  );
}
