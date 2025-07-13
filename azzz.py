import React, { useState } from 'react';

const PhysicsCalculator = () => {
  const [wantToFind, setWantToFind] = useState('');
  const [knownValues, setKnownValues] = useState({});
  const [inputs, setInputs] = useState({});
  const [result, setResult] = useState(null);
  const [formula, setFormula] = useState('');

  const variables = {
    v0: '처음 속도 (v₀)',
    v: '나중 속도 (v)',
    a: '가속도 (a)',
    t: '이동 시간 (t)',
    s: '변위 (s)'
  };

  // 물리적으로 유효한 값인지 검증하는 함수
  const validatePhysicalValues = (values) => {
    const { v0, v, a, t, s } = values;
    
    // 시간은 음수일 수 없음
    if (t !== undefined && t < 0) {
      return { valid: false, reason: "시간은 음수일 수 없습니다." };
    }
    
    // 제곱근 안의 값이 음수가 되는 경우 체크
    if (v0 !== undefined && a !== undefined && s !== undefined) {
      const vSquared = v0 * v0 + 2 * a * s;
      if (vSquared < 0) {
        return { valid: false, reason: "v² = v₀² + 2as에서 v²이 음수가 됩니다. 물리적으로 불가능한 조건입니다." };
      }
    }
    
    if (v !== undefined && a !== undefined && s !== undefined) {
      const v0Squared = v * v - 2 * a * s;
      if (v0Squared < 0) {
        return { valid: false, reason: "v₀² = v² - 2as에서 v₀²이 음수가 됩니다. 물리적으로 불가능한 조건입니다." };
      }
    }
    
    // 이차방정식의 판별식이 음수인 경우
    if (s !== undefined && v0 !== undefined && a !== undefined) {
      const discriminant = v0 * v0 + 2 * a * s;
      if (discriminant < 0) {
        return { valid: false, reason: "주어진 조건으로는 실제 시간을 구할 수 없습니다. (판별식이 음수)" };
      }
    }
    
    return { valid: true };
  };

  // 특정 값을 구하기 위해 필요한 최소 정보를 반환하는 함수
  const getRequiredInfo = (target) => {
    const requirements = {
      'v': [
        'v₀, a, t',
        'v₀, a, s'
      ],
      'v0': [
        'v, a, t',
        'v, a, s'
      ],
      'a': [
        'v, v₀, t',
        'v, v₀, s'
      ],
      't': [
        'v, v₀, a',
        's, v₀, a'
      ],
      's': [
        'v₀, t, a',
        'v, v₀, a'
      ]
    };
    
    return requirements[target] || [];
  };

  const handleKnownValueChange = (variable, isKnown) => {
    setKnownValues(prev => ({
      ...prev,
      [variable]: isKnown
    }));
    
    if (!isKnown) {
      setInputs(prev => {
        const newInputs = { ...prev };
        delete newInputs[variable];
        return newInputs;
      });
    }
  };

  const handleInputChange = (variable, value) => {
    setInputs(prev => ({
      ...prev,
      [variable]: parseFloat(value) || 0
    }));
    
    // 입력값이 변경될 때마다 결과 초기화
    setResult(null);
    setFormula('');
  };

  const calculateResult = () => {
    let workingValues = { ...inputs };
    let calculationSteps = [];
    let finalResult = null;

    try {
      // 초기 입력값 검증
      const initialValidation = validatePhysicalValues(workingValues);
      if (!initialValidation.valid) {
        setResult({
          value: `구할 수 없습니다: ${initialValidation.reason}`,
          steps: []
        });
        setFormula('');
        return;
      }

      // 최대 10번까지 반복하여 값들을 계산 (무한루프 방지)
      for (let iteration = 0; iteration < 10; iteration++) {
        let newValueFound = false;

        // v 계산
        if (workingValues.v === undefined) {
          if (workingValues.v0 !== undefined && workingValues.a !== undefined && workingValues.t !== undefined) {
            workingValues.v = workingValues.v0 + workingValues.a * workingValues.t;
            calculationSteps.push(`v = v₀ + at = ${workingValues.v0} + ${workingValues.a} × ${workingValues.t} = ${workingValues.v.toFixed(3)}`);
            newValueFound = true;
          } else if (workingValues.v0 !== undefined && workingValues.a !== undefined && workingValues.s !== undefined) {
            const vSquared = workingValues.v0 * workingValues.v0 + 2 * workingValues.a * workingValues.s;
            if (vSquared >= 0) {
              workingValues.v = Math.sqrt(vSquared);
              calculationSteps.push(`v² = v₀² + 2as = ${workingValues.v0}² + 2 × ${workingValues.a} × ${workingValues.s} = ${vSquared.toFixed(3)}`);
              calculationSteps.push(`v = √${vSquared.toFixed(3)} = ${workingValues.v.toFixed(3)}`);
              newValueFound = true;
            } else {
              setResult({
                value: "구할 수 없습니다: v²이 음수가 되어 물리적으로 불가능합니다.",
                steps: calculationSteps
              });
              setFormula('');
              return;
            }
          }
        }

        // v0 계산
        if (workingValues.v0 === undefined) {
          if (workingValues.v !== undefined && workingValues.a !== undefined && workingValues.t !== undefined) {
            workingValues.v0 = workingValues.v - workingValues.a * workingValues.t;
            calculationSteps.push(`v₀ = v - at = ${workingValues.v} - ${workingValues.a} × ${workingValues.t} = ${workingValues.v0.toFixed(3)}`);
            newValueFound = true;
          } else if (workingValues.v !== undefined && workingValues.a !== undefined && workingValues.s !== undefined) {
            const v0Squared = workingValues.v * workingValues.v - 2 * workingValues.a * workingValues.s;
            if (v0Squared >= 0) {
              workingValues.v0 = Math.sqrt(v0Squared);
              calculationSteps.push(`v₀² = v² - 2as = ${workingValues.v}² - 2 × ${workingValues.a} × ${workingValues.s} = ${v0Squared.toFixed(3)}`);
              calculationSteps.push(`v₀ = √${v0Squared.toFixed(3)} = ${workingValues.v0.toFixed(3)}`);
              newValueFound = true;
            } else {
              setResult({
                value: "구할 수 없습니다: v₀²이 음수가 되어 물리적으로 불가능합니다.",
                steps: calculationSteps
              });
              setFormula('');
              return;
            }
          }
        }

        // a 계산
        if (workingValues.a === undefined) {
          if (workingValues.v !== undefined && workingValues.v0 !== undefined && workingValues.t !== undefined && workingValues.t !== 0) {
            workingValues.a = (workingValues.v - workingValues.v0) / workingValues.t;
            calculationSteps.push(`a = (v - v₀) / t = (${workingValues.v} - ${workingValues.v0}) / ${workingValues.t} = ${workingValues.a.toFixed(3)}`);
            newValueFound = true;
          } else if (workingValues.v !== undefined && workingValues.v0 !== undefined && workingValues.s !== undefined && workingValues.s !== 0) {
            workingValues.a = (workingValues.v * workingValues.v - workingValues.v0 * workingValues.v0) / (2 * workingValues.s);
            calculationSteps.push(`a = (v² - v₀²) / 2s = (${workingValues.v}² - ${workingValues.v0}²) / (2 × ${workingValues.s}) = ${workingValues.a.toFixed(3)}`);
            newValueFound = true;
          }
        }

        // t 계산
        if (workingValues.t === undefined) {
          if (workingValues.v !== undefined && workingValues.v0 !== undefined && workingValues.a !== undefined && workingValues.a !== 0) {
            const calculatedT = (workingValues.v - workingValues.v0) / workingValues.a;
            if (calculatedT >= 0) {
              workingValues.t = calculatedT;
              calculationSteps.push(`t = (v - v₀) / a = (${workingValues.v} - ${workingValues.v0}) / ${workingValues.a} = ${workingValues.t.toFixed(3)}`);
              newValueFound = true;
            } else {
              setResult({
                value: "구할 수 없습니다: 계산된 시간이 음수입니다.",
                steps: calculationSteps
              });
              setFormula('');
              return;
            }
          } else if (workingValues.s !== undefined && workingValues.v0 !== undefined && workingValues.a !== undefined && workingValues.a !== 0) {
            // s = v₀t + ½at² → ½at² + v₀t - s = 0
            const a_coef = 0.5 * workingValues.a;
            const b_coef = workingValues.v0;
            const c_coef = -workingValues.s;
            const discriminant = b_coef * b_coef - 4 * a_coef * c_coef;
            
            if (discriminant >= 0) {
              const t1 = (-b_coef + Math.sqrt(discriminant)) / (2 * a_coef);
              const t2 = (-b_coef - Math.sqrt(discriminant)) / (2 * a_coef);
              
              // 양수인 시간만 선택
              if (t1 >= 0 && t2 >= 0) {
                workingValues.t = Math.min(t1, t2); // 더 작은 양수값 선택
              } else if (t1 >= 0) {
                workingValues.t = t1;
              } else if (t2 >= 0) {
                workingValues.t = t2;
              } else {
                setResult({
                  value: "구할 수 없습니다: 양수인 시간값을 구할 수 없습니다.",
                  steps: calculationSteps
                });
                setFormula('');
                return;
              }
              
              calculationSteps.push(`s = v₀t + ½at² (이차방정식 해)`);
              calculationSteps.push(`t = ${workingValues.t.toFixed(3)}`);
              newValueFound = true;
            } else {
              setResult({
                value: "구할 수 없습니다: 실근이 존재하지 않습니다.",
                steps: calculationSteps
              });
              setFormula('');
              return;
            }
          }
        }

        // s 계산
        if (workingValues.s === undefined) {
          if (workingValues.v0 !== undefined && workingValues.t !== undefined && workingValues.a !== undefined) {
            workingValues.s = workingValues.v0 * workingValues.t + 0.5 * workingValues.a * workingValues.t * workingValues.t;
            calculationSteps.push(`s = v₀t + ½at² = ${workingValues.v0} × ${workingValues.t} + ½ × ${workingValues.a} × ${workingValues.t}² = ${workingValues.s.toFixed(3)}`);
            newValueFound = true;
          } else if (workingValues.v !== undefined && workingValues.v0 !== undefined && workingValues.a !== undefined && workingValues.a !== 0) {
            workingValues.s = (workingValues.v * workingValues.v - workingValues.v0 * workingValues.v0) / (2 * workingValues.a);
            calculationSteps.push(`s = (v² - v₀²) / 2a = (${workingValues.v}² - ${workingValues.v0}²) / (2 × ${workingValues.a}) = ${workingValues.s.toFixed(3)}`);
            newValueFound = true;
          }
        }

        // 계산 후 매번 물리적 유효성 검증
        const validation = validatePhysicalValues(workingValues);
        if (!validation.valid) {
          setResult({
            value: `구할 수 없습니다: ${validation.reason}`,
            steps: calculationSteps
          });
          setFormula('');
          return;
        }

        // 새로운 값이 발견되지 않으면 반복 종료
        if (!newValueFound) break;

        // 원하는 값이 계산되었는지 확인
        if (workingValues[wantToFind] !== undefined) {
          finalResult = workingValues[wantToFind];
          break;
        }
      }

      if (finalResult !== null) {
        setResult({
          value: finalResult,
          steps: calculationSteps
        });
        setFormula('단계별 계산 과정');
      } else {
        setResult({
          value: '구할 수 없습니다. 필요한 정보가 부족합니다.',
          steps: []
        });
        setFormula('');
      }
    } catch (error) {
      setResult({
        value: '계산 오류가 발생했습니다.',
        steps: []
      });
      setFormula('');
    }
  };

  const reset = () => {
    setWantToFind('');
    setKnownValues({});
    setInputs({});
    setResult(null);
    setFormula('');
  };

  // 입력값이나 선택이 변경될 때마다 결과 초기화
  React.useEffect(() => {
    setResult(null);
    setFormula('');
  }, [wantToFind, knownValues]);

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h1 className="text-3xl font-bold text-center mb-8 text-blue-600">고전 역학 계산기</h1>
      
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4 text-gray-700">너가 구하고 싶은게 뭐야?</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {Object.entries(variables).map(([key, label]) => (
            <label key={key} className="flex items-center space-x-2 cursor-pointer">
              <input
                type="radio"
                name="wantToFind"
                value={key}
                checked={wantToFind === key}
                onChange={(e) => setWantToFind(e.target.value)}
                className="w-4 h-4 text-blue-600"
              />
              <span className="text-gray-700">{label}</span>
            </label>
          ))}
        </div>
      </div>

      {wantToFind && (
        <div className="mb-6">
          <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200 mb-6">
            <h3 className="text-md font-semibold mb-2 text-yellow-800">
              {variables[wantToFind]}을(를) 구하려면 최소한 이러한 정보들이 필요합니다:
            </h3>
            <div className="space-y-1">
              {getRequiredInfo(wantToFind).map((requirement, index) => (
                <p key={index} className="text-sm text-yellow-700">
                  • {requirement}
                </p>
              ))}
            </div>
          </div>

          <h2 className="text-xl font-semibold mb-4 text-gray-700">너가 아는 정보는 뭐야?</h2>
          <div className="space-y-4">
            {Object.entries(variables).map(([key, label]) => {
              if (key === wantToFind) return null;
              
              return (
                <div key={key} className="flex items-center space-x-4">
                  <label className="flex items-center space-x-2 cursor-pointer min-w-[160px]">
                    <input
                      type="checkbox"
                      checked={knownValues[key] || false}
                      onChange={(e) => handleKnownValueChange(key, e.target.checked)}
                      className="w-4 h-4 text-blue-600"
                    />
                    <span className="text-gray-700">{label}</span>
                  </label>
                  
                  {knownValues[key] && (
                    <input
                      type="number"
                      step="any"
                      placeholder="값을 입력하세요"
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      onChange={(e) => handleInputChange(key, e.target.value)}
                    />
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {wantToFind && Object.keys(knownValues).some(key => knownValues[key]) && (
        <div className="mb-8">
          <div className="flex space-x-4">
            <button
              onClick={calculateResult}
              className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
            >
              계산하기
            </button>
            <button
              onClick={reset}
              className="px-6 py-3 bg-gray-500 text-white rounded-md hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 transition-colors"
            >
              초기화
            </button>
          </div>
        </div>
      )}

      {result !== null && (
        <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
          <h3 className="text-lg font-semibold mb-3 text-blue-800">계산 결과</h3>
          <p className="text-2xl font-bold text-blue-600 mb-4">
            {variables[wantToFind]}: {typeof result.value === 'number' ? result.value.toFixed(3) : result.value}
          </p>
        </div>
      )}
    </div>
  );
};

export default PhysicsCalculator;
