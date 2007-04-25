#include <string>

#include "errors.hxx"

Pyx12::EngineError::EngineError(std::string err_str_) {
    err_str = err_str_;
}

std::string
Pyx12::EngineError::what()
{
    return err_str;
}
