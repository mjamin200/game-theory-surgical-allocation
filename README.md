# Game Theory Project: Surgical Procedure Allocation

In this project, we address the allocation of surgical procedures in medical centers a, b, and c, each offering three types of surgeries: A, B, and C. We assume that the time required for surgeries at these medical centers follows a Gaussian random variable with means of 10, 5, and 2 hours, respectively, under normal surgery rates. Since different surgeons perform different types of surgeries at medical centers, the time and cost of procedures vary. Additionally, the arrival rates of each type of surgery at the medical centers differ, with requests following Poisson distributions.

Requests are queued, and the DA algorithm is used to allocate surgical requests to medical centers. In the first step, requests cannot be delayed, but in the second step, requests can delay their turn up to K times if they do not receive immediate attention.

This project is implemented in Python.

## Approach

1. **Input Generation**: Generate surgical request data considering the arrival rates and types of surgeries at each medical center.
2. **DA Algorithm Implementation**: Implement the DA algorithm for surgical procedure allocation to medical centers.
3. **Simulation**: Simulate the allocation process considering the constraints and parameters of the problem.
4. **Performance Evaluation**: Evaluate the performance of the allocation algorithm in terms of efficiency and fairness.
5. **Parameter Tuning**: Tune parameters such as the maximum delay allowance (K) to optimize the allocation process.
6. **Results Analysis**: Analyze the results to identify any patterns or areas for improvement.

## Implementation Details

- Python scripts for data generation, algorithm implementation, and simulation.
- Detailed comments and documentation within the code to explain the logic and functionality.
- Usage instructions and examples provided to facilitate easy understanding and usage of the project.

## Contact

For any questions or inquiries, please contact:

Mohammad Javad Amin
- M.j.amin200@gamil.com

We hope you find this project insightful and useful for understanding surgical procedure allocation in medical centers using game theory principles. Happy coding!
