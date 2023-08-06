# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dlkoopman']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.23.0,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'shortuuid>=1.0.9,<2.0.0',
 'torch>=1.12.1,<2.0.0',
 'tqdm>=4.61.1,<5.0.0']

setup_kwargs = {
    'name': 'dlkoopman',
    'version': '1.0.0',
    'description': 'A Python package for Koopman theory using deep learning.',
    'long_description': 'A Python package for Koopman theory using deep learning.\n\n\n## Table of Contents\n- [Overview](#overview)\n    - [Key features](#key-features)\n    - [Why dlkoopman?](#why-dlkoopman)\n- [Installation](#installation)\n    - [With pip](#with-pip-for-regular-users)\n    - [From source](#from-source-for-development)\n- [Tutorials and Examples](#tutorials-and-examples)\n- [Documentation and API Reference](#documentation-and-api-reference)\n- [Description](#description)\n    - [Koopman theory](#koopman-theory)\n    - [dlkoopman training](#dlkoopman-training)\n    - [dlkoopman prediction](#dlkoopman-prediction)\n- [Known issues](#known-issues)\n- [How to cite](#how-to-cite)\n- [References](#references)\n- [Distribution Statement](#distribution-statement)\n\n\n## Overview\nKoopman theory is a mathematical technique to achieve data-driven approximations of nonlinear dynamical systems by encoding them into a linear space. `dlkoopman` uses deep learning to learn such an encoding, while simultaneously learning the linear dynamics.\n\n### Key features\n- State prediction (`StatePred`) - Train on individual states (snapshots) of a system, then predict unknown states.\n    - E.g: What is the pressure vector on this aircraft for $23.5^{\\circ}$ angle of attack?\n- Trajectory prediction (`TrajPred`) - Train on generated trajectories of a system, then predict unknown trajectories for new initial states.\n    - E.g: What is the behavior of this pendulum if I start from the point $[1,-1]$?\n- General and reusable - supports data from any dynamical system.\n- Novel error function Average Normalized Absolute Error (ANAE) for visualizing performance.\n- Extensive options and a ready-to-use *hyperparameter search module* to improve performance.\n- Built using [Pytorch](https://pytorch.org/), supports both CPU and GPU platforms.\n\n### Why dlkoopman?\nWe bridge the gap between a) software packages that restrict the learning of a good linearizable encoding (e.g. [`pykoopman`](https://github.com/dynamicslab/pykoopman)), and b) efforts that learn encodings for specific applications instead of being a general tool (e.g. [`DeepKoopman`](https://github.com/BethanyL/DeepKoopman)).\n\n\n## Installation\n\n### With pip (for regular users)\n`pip install dlkoopman`\n\n### From source (for development)\n```\ngit clone https://github.com/GaloisInc/dlkoopman.git\ncd dlkoopman\npip install .\n```\n\n\n## Tutorials and examples\nAvailable in the [`examples`](./examples/) folder.\n\n\n## Documentation and API Reference\nAvailable at https://galoisinc.github.io/dlkoopman/.\n\n\n## Description \n\n### Koopman theory\nAssume a dynamical system $x_{i+1} = F(x_i)$, where $x$ is the (genrally multi-dimensional) state of the system at index $i$, and $F$ is the (generally nonlinear) evolution rule describing the dynamics of the system. Koopman theory attempts to *encode* $x$ into a different space $y = g(x)$ where the dynamics are linear, i.e. $y_{i+1} = Ky_i$, where $K$ is the Koopman matrix. This is incredibly powerful since the state $y_i$ at any index $i$ can be predicted from the initial state $y_0$ as $y_i = K^iy_0$. This is then *decoded* back into the original space as $x = g^{-1}(y)$.\n\nFor a thorough mathematical treatment, refer to [`koopman_theory.pdf`](./koopman_theory.pdf).\n\n### dlkoopman training\n<figure><center>\n<img src="training_architecture.png" width=750/>\n</center></figure>\n\nThis is a small example with three input states $\\left[x_0, x_1, x_2\\right]$. These are passed through an encoder neural network to get encoded states $\\left[y_0, y_1, y_2\\right]$. These are passed through a decoder neural network to get $\\left[\\hat{x}_0, \\hat{x}_1, \\hat{x}_2\\right]$, and also used to learn $K$. This is used to derive predicted encoded states $\\left[\\mathsf{y}_1, \\mathsf{y}_2\\right]$, which are then passed through the same decoder to get predicted approximations $\\left[\\hat{\\mathsf{x}}_1, \\hat{\\mathsf{x}}_2\\right]$ to the original input states.\n\nErrors mimimized during training:\n- Train the autoencoder - Reconstruction `recon` between $x$ and $\\hat{x}$.\n- Train the Koopman matrix - Linearity `lin` between $y$ and $\\mathsf{y}$.\n- Combine the above - Prediction `pred` between $x$ and $\\hat{\\mathsf{x}}$.\n\n### dlkoopman prediction\n<figure><center>\n<img src="prediction_architecture.png" width=750/>\n</center></figure>\n\nPrediction happens after training.\n\n(a) State prediction - Compute predicted states for new indexes such as $i\'$. This uses the eigendecomposition of $K$, so $i\'$ can be any real number - positive (forward extapolation), negative (backward extrapolation), or fractional (interpolation).\n\n(b) Trajectory prediction - Generate predicted trajectories $j\'$ for new starting states such as $x^{j\'}_0$. This uses a linear neural net layer to evolve the initial state.\n\n\n## Known issues\nSome common issues and ways to overcome them are described in the [known issues](https://github.com/GaloisInc/dlkoopman/issues?q=is%3Aissue+is%3Aclosed+label%3Aknown-issue).\n\n\n## How to cite\nPlease cite the accompanying paper:\n```\n@article{Dey2022_dlkoopman,\n    author = {Sourya Dey and Eric Davis},\n    title = {DLKoopman: A deep learning software package for Koopman theory},\n    year = {2022},\n    note = {Submitted to 5th Annual Learning for Dynamics & Control (L4DC) Conference}\n}\n```\n\n\n## References\n- B. O. Koopman - Hamiltonian systems and transformation in Hilbert space\n- J. Nathan Kutz, Steven L. Brunton, Bingni Brunton, Joshua L. Proctor - Dynamic Mode Decomposition\n- Bethany Lusch, J. Nathan Kutz & Steven L. Brunton - Deep learning for universal linear embeddings of nonlinear dynamics\n\n\n## Distribution Statement\nThis material is based upon work supported by the United States Air Force and DARPA under Contract No. FA8750-20-C-0534. Any opinions, findings and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the United States Air Force and DARPA. Distribution Statement A, "Approved for Public Release, Distribution Unlimited."\n',
    'author': 'Sourya Dey',
    'author_email': 'sourya@galois.com',
    'maintainer': 'Galois dlkoopman team',
    'maintainer_email': 'dlkoopman@galois.com',
    'url': 'https://github.com/GaloisInc/dlkoopman',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
